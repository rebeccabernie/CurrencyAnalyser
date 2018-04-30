""" 
Script that pulls prices and rates of specified currencies using forex python.
The data is then formatted and published via redis. 
It would be cumbersome to query and reformat the query result with every api request, 
especially since the requests are rarely dependant on external inputs.
this way the preformatted data can be accessed easily and quickly by redis every request.
"""
import redis, json, time, datetime, config
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
from forex_python.bitcoin import BtcConverter

r = redis.from_url(config.REDIS_URL)
tic = 30.0
latest_currencies = {
    'currencies': []
}
chart_data = {
    'labels': [],
    'datasets': []
}

"""
Hard coded list of colours instead to ensure colour diversity. 

# Generate a unique colour based on unique currency code.
# Get the ASCII code values for the char's A-Y are 65-90.
def rgbChar(c):
    return str(int((((ord(c)-65)/25)*255)))
"""

time.sleep(60 - datetime.datetime.now().second)
starttime = time.time()

def pullData():
    t = '{:%H:%M:%S}'.format(datetime.datetime.now() + datetime.timedelta(hours=1))
    #t = time.strftime("%H:%M:%S")
    print("Starting at number: " + str(datetime.datetime.utcnow()))
    # Using forex to get latest data: https://media.readthedocs.org/pdf/forex-python/latest/forex-python.pdf
    c = CurrencyRates()
    b = BtcConverter()
    rates = c.get_rates(config.LOCAL_CURR_CODE)
    pop = False

    # Adapted from: https://stackoverflow.com/questions/30071886/how-to-get-current-time-in-python-and-break-up-into-year-month-day-hour-minu
    chart_data['labels'].append(t)
    # If 20 dates are already currently in the list - pop.
    if len(chart_data['labels']) >= 20:
        chart_data['labels'].pop(0)
        pop = True
    # Loop through array of datasets to append or append and pop.
    if chart_data['datasets']:
        for i, code in enumerate(config.CURR_CODES):
            if code == 'BTC':
                price = round(b.get_latest_price(config.LOCAL_CURR_CODE),2)
                rate = round(b.convert_to_btc(1, config.LOCAL_CURR_CODE),5)
            else:
                price = round(c.get_rate(code, config.LOCAL_CURR_CODE),2)
                rate = round(rates[chart_data['datasets'][i]['label']],5)
            chart_data['datasets'][i]['data'].append(price)
            latest_currencies['currencies'][i]['data'] = rate
            if pop:
                chart_data['datasets'][i]['data'].pop(0)
    else:
        co = CurrencyCodes()
        # Prepare data objects and pull first prices.
        for i, code in enumerate(config.CURR_CODES):
            if code == 'BTC':
                symbol = b.get_symbol()
                name = 'Bitcoin'
                price = round(b.get_latest_price(config.LOCAL_CURR_CODE),2)
                rate = round(b.convert_to_btc(1, config.LOCAL_CURR_CODE),5)
            else:
                name = co.get_currency_name(code)
                symbol = co.get_symbol(code)
                price = round(c.get_rate(code, config.LOCAL_CURR_CODE),2)
                rate = round(rates[code], 5)
            chart_data['datasets'].append({
                'label': code,
                'backgroundColor': config.CURR_COLORS[i],
                'data': [price]
            })
            latest_currencies['currencies'].append({
                'code': code,
                'name': name,
                'symbol': symbol,
                'data': rate
            })

    r.set(config.REDIS_CHAN_LIST, latest_currencies)
    r.set(config.REDIS_CHAN_GRAPH, chart_data)
    
    print("Finishing at number: " + str(datetime.datetime.utcnow()))

while True:
    pullData()
    # Adapted from: https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/38317060
    time.sleep(tic - ((time.time() - starttime) % tic))