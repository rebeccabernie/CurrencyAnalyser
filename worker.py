import redis
import json

#from Web import REDIS_URL, REDIS_CHAN
from time import sleep

REDIS_URL = "redis://localhost:6379" 
REDIS_CHAN = "test"

r = redis.from_url(REDIS_URL)
print("connected")
num = 0
while(True):
    print("publishing num: " + str(num))
    payload = json.dumps({
        'value': num,
        })
    r.publish(REDIS_CHAN, payload)
    num +=1
    sleep(1)