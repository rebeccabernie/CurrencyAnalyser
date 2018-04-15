import os

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379') #"redis://localhost:6379" 
REDIS_CHAN_GRAPH = "currencygraph"
REDIS_CHAN_LIST = "currencylatest"

CURR_CODES = ['AUD', 'BTC', 'CAD', 'CHF', 'CNY', 'GBP', 'HKD', 'IDR', 'JPY', 'KRW', 'USD', 'ZAR']
CURR_COLORS = ['rgba(97, 226, 61, 0.75)', 'rgba(255, 188, 32, 0.75)', 'rgba(232, 22, 0, 0.75)', 'rgba(255, 132, 33, 0.75)', 'rgba(60, 226, 146, 0.75)', 'rgba(88, 226, 190, 0.75)', 'rgba(88, 131, 226, 0.75)', 'rgba(129, 88, 226,0.75)', 'rgba(206, 80, 135,0.75)', 'rgba(206, 80, 80,0.75)', 'rgba(193, 7, 7, 0.75)', 'rgba(155, 79, 79,0.75)']