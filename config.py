import os

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379') #"redis://localhost:6379" 
REDIS_CHAN_CURR = "currency"
REDIS_CHAN_GRAPH = "currencygraph"
REDIS_CHAN_LIST = "currencylatest"

CURR_CODES = ['BTC', 'AUD', 'CAD', 'CHF', 'CNY', 'GBP', 'HKD', 'IDR', 'JPY', 'KRW', 'USD', 'ZAR']
CURR_NAMES = ['Bitcoin', 'Australian Dollar', 'Canadian Dollar', 'Swiss Franc', 'Chinese Yuan', 'British Pound', 'Hong Kong Dollar', 'Indian Rupee', 'Japanese Ken', 'South Korean Won', 'US Dollar', 'South African Rand']