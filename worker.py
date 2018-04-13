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

tic = 60.0
starttime=time.time()

while True:
    print("Starting at number: " + str(datetime.datetime.utcnow()))

    # Using forex to get latest data: https://media.readthedocs.org/pdf/forex-python/latest/forex-python.pdf
    c = CurrencyRates()
    b = BtcConverter()
    data = c.get_rates('USD')
    rates = DictHelper(data)

    for (key, value) in rates.items():
        print(key, value)
    
    chart = json.dumps({
        'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'datasets': 
        [{
            'label': 'EURO',
            'backgroundColor': 'rgba(255, 0, 0, 0.5)',
            'data': [randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100)]
        },
        {
            'label': 'BITCOIN',
            'backgroundColor': 'rgba(169,169,169, 0.5)',
            'data': [randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100)]
        }]
        })

    r.set(REDIS_CHAN_GRAPH, chart)
    
    print("Finishing at number: " + str(datetime.datetime.utcnow()))
    # Adapted from: https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/38317060
    time.sleep(tic - ((time.time() - starttime) % tic))