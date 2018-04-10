import redis
import json
import atexit

#from Web import REDIS_URL, REDIS_CHAN
from time import sleep

REDIS_URL = "redis://localhost:6379" 
REDIS_CHAN = "test"

r = redis.from_url(REDIS_URL)
print("connected")

# Adapted from: https://docs.python.org/2/library/atexit.html
@atexit.register
def goodbye():
    payload = 'KILL'
    r.publish(REDIS_CHAN, payload)

num = 0
while(True):
    print("publishing num: " + str(num))
    payload = json.dumps({
        'value': num,
        })
    r.publish(REDIS_CHAN, payload)
    num +=1
    sleep(1)