#Forex data
from forex_python.converter import CurrencyRates
#Bitcoin data, provided by coin desk
from forex_python.bitcoin import BtcConverter

import time
import schedule
import os
import redis

rds = redis.from_url(os.environ.get("REDIS_URL"))

def siphon():
  #Converters
  c = CurrencyRates()
  b = BtcConverter()

  #USD TO EURO
  usd_float = c.get_rate('USD', 'EUR')
  #Bitcoin IN EURO
  btc_float = b.get_latest_price('EUR')

  usd = "{:.4f}".format(usd_float) 
  btc = "{:.4f}".format(btc_float) 

  
  rds.set('1',usd)
  rds.set('2', btc)

  u = rds.get(1).decode(encoding='UTF-8')
  b = rds.get(2).decode(encoding='UTF-8')

  #Output to console
  print("Price of US Dolar in Euro: "+ u)
  print("Price of Bitcoin in Euro: "+ b)



schedule.every(10).seconds.do(siphon)

while 1:
    schedule.run_pending()
    time.sleep(1)
