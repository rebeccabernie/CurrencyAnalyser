import redis
import json
import atexit
from random import randint

from time import sleep
from config import REDIS_URL, REDIS_CHAN_CURR, REDIS_CHAN_GRAPH

r = redis.from_url(REDIS_URL)

# Adapted from: https://docs.python.org/2/library/atexit.html
@atexit.register
def goodbye():
    print("Shutting down")
    print("Killing listener")
    payload = 'KILL'
    r.publish(REDIS_CHAN_CURR, payload)

num = 0
while(True):
    print("Publishing number: " + str(num))
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
    #r.publish(REDIS_CHAN_CURR, payload)
    r.set(REDIS_CHAN_GRAPH, chart)
    num +=1
    sleep(1)