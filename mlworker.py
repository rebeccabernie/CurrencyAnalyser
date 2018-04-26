import btcmodel, time, config, redis, pymongo
from datetime import date, timedelta, datetime
from pymongo import MongoClient

# Set up database connections
r = redis.from_url(config.REDIS_URL)
m = MongoClient(config.MONGO_URL)

# Seconds in a day.
tic = 86400

# Create and build model.
btc = btcmodel.BTCModel(m, r)

# Predict today's close price and publish to redis.
''' TODO: change timedelta param to 1'''
''' TODO: publish to redis'''
''' TODO: set up chart data'''
btc.predict((date.today() - timedelta(2)).strftime("%Y%m%d"))


# Wait till 3am.
# Adapted from: https://stackoverflow.com/questions/36810003/python-calculate-seconds-from-now-to-specified-time-today-or-tomorrow
# now = datetime.now()
# time.sleep((timedelta(hours=24) - (now - now.replace(hour=3, minute=00, second=0, microsecond=0))).total_seconds() % (24 * 3600))

# Start loop.
starttime = time.time()
# while True:

# If not prevously predicted: predict yesterday's close price.
if btc.getPrediction() == None:
    ''' TODO: change timedelta param to 2'''
    btc.predict((date.today() - timedelta(3)).strftime("%Y%m%d"))

# Train with yesterday's predicted and yesterday's actual close price.
btc.train()

# Predict today's close price.
''' TODO: change timedelta param to 1'''
btc.predict((date.today() - timedelta(2)).strftime("%Y%m%d"))

btc.refreshchart()

# Sleep thread until tomorrow at 3am.
#time.sleep(tic - ((time.time() - starttime) % tic))