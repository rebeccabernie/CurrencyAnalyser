import redis, json, atexit, time
from random import randint
from config import REDIS_URL, REDIS_CHAN_CURR, REDIS_CHAN_GRAPH

from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import datetime, schedule, os

r = redis.from_url(REDIS_URL)

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