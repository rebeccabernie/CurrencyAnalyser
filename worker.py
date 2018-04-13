import redis, json, atexit, time
from random import randint
from config import REDIS_URL, REDIS_CHAN_CURR, REDIS_CHAN_GRAPH

from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import datetime, schedule, os

r = redis.from_url(REDIS_URL)

# Adapted: https://stackoverflow.com/questions/29033259/how-to-iterate-over-dict-in-class-like-if-just-referring-to-dict
class DictHelper(dict):
        def __init__(self, *arg, **kw):
            super(DictHelper, self).__init__(*arg, **kw)
            self.choosebettername = super(DictHelper, self).keys()

        def __iter__(self):
            return iter(self.choosebettername)

        def keys(self):
            return self.choosebettername

        def itervalues(self):
            return (self[key] for key in self)

# Adapted from: https://docs.python.org/2/library/atexit.html
@atexit.register
def goodbye():
    print("Shutting down")
    """
    print("Killing listener")
    payload = 'KILL'
    r.publish(REDIS_CHAN_CURR, payload)
    """

tic = 30.0
starttime = time.time()

# Generate a unique colour based on unique currency code.
# Get the ASCII code values for the char's A-Y are 65-90
def rgbChar(c):
    return str((((ord(c)-65)/25)*255))

while True:
    print("Starting at number: " + str(datetime.datetime.utcnow()))

    # Using forex to get latest data: https://media.readthedocs.org/pdf/forex-python/latest/forex-python.pdf
    c = CurrencyRates()
    b = BtcConverter()

    chart_data = {
        'labels': [],
        'datasets': 
        []
        }
    
    data = c.get_rates('USD')
    rates = DictHelper(data)

    # Adapted from: https://stackoverflow.com/questions/30071886/how-to-get-current-time-in-python-and-break-up-into-year-month-day-hour-minu
    chart_data['labels'].append(time.strftime("%H:%M:%S"))

    for (key, value) in rates.items():
        # print(key, value)
        k = list(key)
        chart_data['datasets'].append({
            'label': key,
            'backgroundColor': 'rgba('+rgbChar(k[0])+','+rgbChar(k[1])+','+rgbChar(k[2])+', 0.65)',
            'data': [value]
        })

    print(chart_data)
    chart = json.dumps(chart_data)
    r.set(REDIS_CHAN_GRAPH, chart)
    
    print("Finishing at number: " + str(datetime.datetime.utcnow()))
    # Adapted from: https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/38317060
    time.sleep(tic - ((time.time() - starttime) % tic))