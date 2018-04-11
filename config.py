import os

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379') #"redis://localhost:6379" 
REDIS_CHAN_CURR = "currency"
REDIS_CHAN_GRAPH = "currencygraph"