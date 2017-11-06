#Forex data
from forex_python.converter import CurrencyRates
#Bitcoin data, provided by coin desk
from forex_python.bitcoin import BtcConverter

import time

import schedule

def siphon():
  #Converters
  c = CurrencyRates()
  b = BtcConverter()

  #USD TO EURO
  usd = c.get_rate('USD', 'EUR')
  #Bitcoin IN EURO
  btc = b.get_latest_price('EUR')

  print("Price of US Dolar in Euro: ", usd)
  print("Price of Bitcoin in Euro: ", btc)


schedule.every(20).seconds.do(siphon)

while 1:
    schedule.run_pending()
    time.sleep(1)
#attempt at timed loop
#starttime=time.time()
#while True:
#  print ("tick")
#  time.sleep(60.0 - ((time.time() - starttime) % 60.0))