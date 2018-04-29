import json
import os
from urllib.request import urlopen
import pandas as pd
import numpy as np
import h5py

def collectData():
    url = 'https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=1356998100&end=9999999999&period=300'
    openUrl = urlopen(url)
    r = openUrl.read()
    openUrl.close()
    d = json.loads(r.decode())

    df = pd.DataFrame(d)
    original_columns=[u'close', u'date', u'high', u'low', u'open']
    new_columns = ['Close','Timestamp','High','Low','Open']
    df = df.loc[:,original_columns]
    df.columns = new_columns
    df.head()

    with h5py.File(''.join(['bitcoin2015to2017_wf.h5']), 'r') as hf:
        datas = hf['inputs'].value
        labels = hf['outputs'].value
        input_times = hf['input_times'].value
        output_times = hf['output_times'].value
        original_inputs = hf['original_inputs'].value
        original_outputs = hf['original_outputs'].value
        original_datas = hf['original_datas'].value

    original_inputs[0].shape

    df.to_csv('bitcoin2015to2017.csv',index=None)


def processData():
    input_step_size = 50
    output_size = 30
    sliding_window = False
    file_name= 'bitcoin2012_2017_50_30_prediction.h5' 

    df = pd.read_csv('bitstampUSD_1-min_data_2012-01-01_to_2017-05-31.csv').drop(['Date'], 1)
    df['Datetime'] = pd.to_datetime(df['Timestamp'],unit='s')
    df.head()

    prices= df.loc[:,'Close'].values
    times = df.loc[:,'Close'].values
    prices.shape

    outputs = []
    inputs = []
    output_times = []
    input_times = []
    if sliding_window:
        for i in range(len(prices)-input_step_size-output_size):
            inputs.append(prices[i:i + input_step_size])
            input_times.append(times[i:i + input_step_size])
            outputs.append(prices[i + input_step_size: i + input_step_size+ output_size])
            output_times.append(times[i + input_step_size: i + input_step_size+ output_size])
    else:
        for i in range(0,len(prices)-input_step_size-output_size, input_step_size):
            inputs.append(prices[i:i + input_step_size])
            input_times.append(times[i:i + input_step_size])
            outputs.append(prices[i + input_step_size: i + input_step_size+ output_size])
            output_times.append(times[i + input_step_size: i + input_step_size+ output_size])
    inputs= np.array(inputs)
    outputs= np.array(outputs)
    output_times = np.array(output_times)
    input_times = np.array(input_times)

    with h5py.File(file_name, 'w') as f:
        f.create_dataset("inputs", data = inputs)
        f.create_dataset('outputs', data = outputs)
        f.create_dataset("input_times", data = input_times)
        f.create_dataset('output_times', data = output_times)

collectData()
processData()
