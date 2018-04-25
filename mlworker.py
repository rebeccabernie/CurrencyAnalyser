import btcmodel #, time
from datetime import date, timedelta


btc = btcmodel.BTCModel()
btc.predict((date.today() - timedelta(2)).strftime("%Y%m%d"))
print(btc.getPrediction())
btc.train()

# Pull yesterday:
#   if not null (if it is not between 12am - 3am): 
#       predict   



# Wait till 3/4am

# Start day loop:

#   if not prevously predicted:
#       pull day before yesterday
#       predict

#   pull yesterday actual 
#   train with predict and yesterday actual

#   pull yesterday 
#   predict