import redis, json, time, datetime, schedule, os
from config import REDIS_URL, REDIS_CHAN_CURR, REDIS_CHAN_GRAPH
from dicthelper import DictHelper
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter

r = redis.from_url(REDIS_URL)
tic = 30.0
starttime = time.time()
currencies = []
chart_data = {
        'labels': [],
        'datasets': 
        []
        }

# Generate a unique colour based on unique currency code.
# Get the ASCII code values for the char's A-Y are 65-90.
def rgbChar(c):
    return str((((ord(c)-65)/25)*255))

while True:
    print("Starting at number: " + str(datetime.datetime.utcnow()))

    # Using forex to get latest data: https://media.readthedocs.org/pdf/forex-python/latest/forex-python.pdf
    c = CurrencyRates()
    b = BtcConverter()
    data = c.get_rates('EUR')
    btc = b.get_latest_price('EUR')
    rates = DictHelper(data)
    pop = False

    # Adapted from: https://stackoverflow.com/questions/30071886/how-to-get-current-time-in-python-and-break-up-into-year-month-day-hour-minu
    chart_data['labels'].append(time.strftime("%H:%M:%S"))
    # If 20 dates are already currently in the list - pop.
    if len(chart_data['labels']) >= 20:
        chart_data['labels'].pop(0)
        pop = True
    # Loop through array of datasets to append or append and pop.
    if chart_data['datasets']:
        i = 0
        chart_data['datasets'][i]['data'].append(btc)
        if pop:
            chart_data['datasets'][i]['data'].pop(0)
        for value in rates.values():
            i = i + 1
            chart_data['datasets'][i]['data'].append(value)
            if pop:
                chart_data['datasets'][i]['data'].pop(0)
    else:
        # Set up data set. BTC is done seperately due to the way forex data is queried.
        chart_data['datasets'].append({
            'label': 'BTC',
            'backgroundColor': 'rgba('+rgbChar('Y')+','+rgbChar('T')+','+rgbChar('C')+', 0.65)',
            'data': [btc]
        })
        for (key, value) in rates.items():
            currencies.append(key)
            k = list(key)
            chart_data['datasets'].append({
                'label': key,
                'backgroundColor': 'rgba('+rgbChar(k[0])+','+rgbChar(k[1])+','+rgbChar(k[2])+', 0.65)',
                'data': [value]
            })
        r.set(REDIS_CHAN_CURR, currencies)

    chart = json.dumps(chart_data)
    r.set(REDIS_CHAN_GRAPH, chart)
    
    print("Finishing at number: " + str(datetime.datetime.utcnow()))
    # Adapted from: https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/38317060
    time.sleep(tic - ((time.time() - starttime) % tic))