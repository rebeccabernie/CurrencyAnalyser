import redis
import json
import atexit

from time import sleep
from config import REDIS_URL, REDIS_CHAN

r = redis.from_url(REDIS_URL)

# Adapted from: https://docs.python.org/2/library/atexit.html
@atexit.register
def goodbye():
    print("Shutting down")
    print("Killing listener")
    payload = 'KILL'
    r.publish(REDIS_CHAN, payload)

num = 0
while(True):
    print("Publishing number: " + str(num))
    payload = json.dumps({
        'value': num,
        })
    r.publish(REDIS_CHAN, payload)
    num +=1
    sleep(1)