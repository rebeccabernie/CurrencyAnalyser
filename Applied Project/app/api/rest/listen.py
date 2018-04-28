#import redis
#import json
import threading
#import requests

from time import sleep

from config import REDIS_CHAN_GRAPH

# Adapted from
class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        self.redis.set(REDIS_CHAN_GRAPH, item['data'])
        #print("Item recived: " + str(item['data']))

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == b'KILL':
                self.pubsub.unsubscribe()
                print(self, "unsubsribed")
                break
            else:
                self.work(item)
            #sleep(0.001)