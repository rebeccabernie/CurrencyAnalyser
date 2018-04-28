""" 
Script that pulls market data, builds a model and predicts the current day's closing price.
Every day at 3am, yesterday's actual closing price is pulled and used to further train the model.
The data is then saved to the database and published to the api via redis. The now current day's 
close price can be predicted.
"""
import time, config, redis, pymongo
from datetime import date, timedelta, datetime
from pymongo import MongoClient
from ml import btcmodel

# Set up database connections
r = redis.from_url(config.REDIS_URL)
m = MongoClient(config.MONGO_URL)

# Seconds in a day.
tic = 86400

# Create and build model.
btc = btcmodel.BTCModel(m, r)

# Predict today's close price and publish to redis.
btc.predict((date.today() - timedelta(1)).strftime("%Y%m%d"))


# Wait till 3am.
# Adapted from: https://stackoverflow.com/questions/36810003/python-calculate-seconds-from-now-to-specified-time-today-or-tomorrow
now = datetime.now()
time.sleep((timedelta(hours=24) - (now - now.replace(hour=3, minute=00, second=0, microsecond=0))).total_seconds() % (24 * 3600))

# Start loop.
starttime = time.time()
while True:
    # If not prevously predicted: predict yesterday's close price.
    if btc.getPrediction() == None:
        btc.predict((date.today() - timedelta(2)).strftime("%Y%m%d"))

    # Train with yesterday's predicted and yesterday's actual close price.
    btc.train()

    # Predict today's close price.
    btc.predict((date.today() - timedelta(1)).strftime("%Y%m%d"))

    btc.refreshchart()

    # Sleep thread until tomorrow at 3am.
    time.sleep(tic - ((time.time() - starttime) % tic))