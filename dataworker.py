import redis, json, time, datetime, schedule, os, config
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
    t = time.strftime("%H:%M:%S")
    print("Starting at number: " + str(datetime.datetime.utcnow()))
    # Using forex to get latest data: https://media.readthedocs.org/pdf/forex-python/latest/forex-python.pdf
    c = CurrencyRates()
    b = BtcConverter()
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
                price = '{0:.5f}'.format(b.get_latest_price('EUR'))
            else:
                price = '{0:.5f}'.format(c.get_rate(code, 'EUR'))
            chart_data['datasets'][i]['data'].append(price)
            latest_currencies['currencies'][i]['data'] = price
            if pop:
                chart_data['datasets'][i]['data'].pop(0)
    else:
        co = CurrencyCodes()
        # Prepare data objects and pull first prices.
        for i, code in enumerate(config.CURR_CODES):
            if code == 'BTC':
                symbol = b.get_symbol()
                name = 'Bitcoin'
                price = '{0:.5f}'.format(b.get_latest_price('EUR'))
            else:
                name = co.get_currency_name(code)
                symbol = co.get_symbol(code)
                price = '{0:.5f}'.format(c.get_rate(code, 'EUR'))
            chart_data['datasets'].append({
                'label': code,
                'backgroundColor': config.CURR_COLORS[i],
                'data': [price]
            })
            latest_currencies['currencies'].append({
                'code': code,
                'name': name,
                'symbol': symbol,
                'data': price
            })

    r.set(config.REDIS_CHAN_LIST, latest_currencies)
    r.set(config.REDIS_CHAN_GRAPH, chart_data)
    
    print("Finishing at number: " + str(datetime.datetime.utcnow()))

while True:
    pullData()
    # Adapted from: https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/38317060
    time.sleep(tic - ((time.time() - starttime) % tic))