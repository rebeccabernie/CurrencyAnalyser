import pandas as pd
import time
from datetime import date, timedelta
from model import build_model
import numpy as np

# Change this value if you want to make longer/shorter prediction, i.e. number of days.
pred_range, window_len = 1, 1
bt_model = None

def create():
    # Pull past data, starting from 01/01/2016 (Data is inconsistent before then) -> two days ago
    # Bitcoin market info: "Date", "Open", "High", "Low", "Close", "Volume", "Market Cap". 
    btc_past = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20160101&end="+(date.today() - timedelta(2)).strftime("%Y%m%d"))[0]
    # Convert the date string to the datetime format, and "Volume" to an integer.
    btc_past = btc_past.assign(Date=pd.to_datetime(btc_past['Date']))
    btc_past['Volume'] = btc_past['Volume'].astype('int64')
    # Rename columns.
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
    LSTM_training_outputs = []

    for i in range(len(model_data)-window_len):
        temp_set = model_data[i:(i+window_len)].copy()
        LSTM_training_inputs.append(temp_set)
    LSTM_training_inputs = [np.array(LSTM_training_input) for LSTM_training_input in LSTM_training_inputs]
    LSTM_training_inputs = np.array(LSTM_training_inputs)

    for i in range(window_len, len(model_data['bt_Close'])-pred_range):
        LSTM_training_outputs.append((model_data['bt_Close'][i:i+pred_range].values/
                                    model_data['bt_Close'].values[i-window_len])-1)
    LSTM_training_outputs = np.array(LSTM_training_outputs)

    # Random seed for reproducibility.
    np.random.seed(202)
    # Initialise model architecture and train model with training set.
    bt_model = build_model(LSTM_training_inputs, output_size=pred_range, neurons = 20)
    bt_model.fit(LSTM_training_inputs[:-pred_range], LSTM_training_outputs, 
                                epochs=25, batch_size=1, verbose=2, shuffle=True)