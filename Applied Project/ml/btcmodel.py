import pandas as pd
from datetime import date, timedelta
from ml.model import build_model
import numpy as np
import pymongo, config

class BTCModel:
    # Change this value if you want to make longer/shorter prediction, i.e. number of days.
    pred_range, window_len = 1, 1
    prediction, predict_inputs, predict_data = None, None, None

    def __init__(self, m, r):
        self.m, self.r = m, r
        # Pull past data, starting from 01/01/2016 (Data is inconsistent before then) -> two days ago.
        # Bitcoin market info: "Date", "Open", "High", "Low", "Close", "Volume", "Market Cap". 
        btc_past = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20160101&end="+(date.today() - timedelta(2)).strftime("%Y%m%d"))[0] 
        # Convert the date string to the datetime format, "Volume" to an integer and rename columns.
        btc_past = btc_past.assign(Date=pd.to_datetime(btc_past['Date']))
        btc_past['Volume'] = btc_past['Volume'].astype('int64')
        btc_past.columns =[btc_past.columns[0]]+['bt_'+i for i in btc_past.columns[1:]]
        # Create "Supply" column, to display the circulating supply - i.e. the amount of bitcoins that currently exist. 
        # This is important as the supply or exclusivity should directly affect prices.
        for coins in ['bt_']: 
            kwargs = { coins+'Supply': lambda x: (x[coins+'Market Cap'])/(x[coins+'Close']) }
            btc_past = btc_past.assign(**kwargs)
        # Only keep columns "Close", "Volume", Supply".
        model_data = btc_past[['Date']+[coin+metric for coin in ['bt_'] 
            for metric in ['Close', 'Volume', 'Supply']]]
        # Reverse the data frame so that the row represent the right time frame. Remove "Date" column, since we are now finished with the dates.
        model_data = model_data.sort_values(by='Date')
        model_data = model_data.drop('Date', 1)
        # Prepare training inputs and outputs.
        LSTM_training_inputs = []
        for i in range(len(model_data)-self.window_len):
            temp_set = model_data[i:(i+self.window_len)].copy()
            LSTM_training_inputs.append(temp_set)
        LSTM_training_inputs = [np.array(LSTM_training_input) for LSTM_training_input in LSTM_training_inputs]
        LSTM_training_inputs = np.array(LSTM_training_inputs)
        LSTM_training_outputs = []
        for i in range(self.window_len, len(model_data['bt_Close'])-self.pred_range):
            LSTM_training_outputs.append((model_data['bt_Close'][i:i+self.pred_range].values/
                                        model_data['bt_Close'].values[i-self.window_len])-1)
        LSTM_training_outputs = np.array(LSTM_training_outputs)
        # Random seed for reproducibility.
        np.random.seed(202)
        # Initialise model architecture and train model with training set.
        self.bt_model = build_model(LSTM_training_inputs, output_size=self.pred_range, neurons = 20)
        self.bt_model.fit(LSTM_training_inputs[:-self.pred_range], LSTM_training_outputs, 
                                    epochs=25, batch_size=1, verbose=2, shuffle=True)
   
    def predict(self, day):
        # Aquire and prepare data.
        btc_day = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start="+day+"&end="+day)[0]
        if btc_day.iloc[0]['Date'] != 'No data was found for the selected time period.':
            btc_day = btc_day.assign(Date=pd.to_datetime(btc_day['Date']))
            btc_day['Volume'] = btc_day['Volume'].astype('int64')
            btc_day.columns =[btc_day.columns[0]]+['bt_'+i for i in btc_day.columns[1:]]
            self.predict_data = btc_day
            for coins in ['bt_']: 
                kwargs = { coins+'Supply': lambda x: (x[coins+'Market Cap'])/(x[coins+'Close']) }
                btc_day = btc_day.assign(**kwargs)
            m_data = btc_day[[coin+metric for coin in ['bt_'] 
                                        for metric in ['Close', 'Volume', 'Supply']]]
            self.predict_inputs = []
            for i in range(len(m_data)):
                temp_set = m_data[i:(i+self.window_len)].copy()
                self.predict_inputs.append(temp_set)
            self.predict_inputs = [np.array(self.predict_inputs) for self.predict_inputs in self.predict_inputs]
            self.predict_inputs = np.array(self.predict_inputs)
            self.prediction = (self.bt_model.predict(self.predict_inputs, batch_size=1)+1)*m_data['bt_Close'].values.reshape(1,1)
            if(self.prediction != None):
                self.r.set(config.REDIS_CHAN_ML_BTC, round(self.prediction[0][0], 2))

    def getPrediction(self):
        return self.prediction
    
    def train(self):
        day = (date.today() - timedelta(1)).strftime("%Y%m%d")
        btc_day = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start="+day+"&end="+day)[0]
        if btc_day.iloc[0]['Date'] != 'No data was found for the selected time period.':
            if (self.prediction != None):
                predict_outputs = [[(btc_day.iloc[0]['Close']/self.predict_data.iloc[0]['bt_Close'])-1]]
                predict_outputs = np.array(predict_outputs)
                self.bt_model.train_on_batch(self.predict_inputs, predict_outputs)
                self.m.db.ml.insert({
                    "date" : date.today().strftime("%Y-%m-%d"),
                    "currency" : "btc",
                    "prediction" : round(self.prediction[0][0], 2),
                    "actual" : round(btc_day.iloc[0]['Close'], 2)
                })
                self.prediction, self.predict_inputs, self.predict_data = None, None, None
    def refreshchart(self):
        chart_data = {
            'labels': [],
            'datasets': [
                { 'label': 'prediction', 'backgroundColor': 'rgba(41, 244, 170, 0.75)', 'data': [] },
                { 'label': 'actual', 'backgroundColor': 'rgba(186, 65, 67, 0.75)', 'data': [] }
            ]
        }
        cursor = self.m.db.ml.find().sort('date', pymongo.DESCENDING).limit(20)
        for doc in cursor:
            chart_data['labels'].insert(0, doc['date'])
            chart_data['datasets'][0]['data'].insert(0, doc['prediction'])
            chart_data['datasets'][1]['data'].insert(0, doc['actual'])
        self.r.set(config.REDIS_CHAN_ML_BTC_GRAPH, chart_data)