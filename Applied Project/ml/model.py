from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras import metrics

def build_model(inputs, output_size, neurons, activ_func="linear",
                dropout=0.25, loss="mae", optimizer="adam"):
    model = Sequential()
    
    # Use LSTM(Long Short Term Memory) an efficient, gradient-based Model introduced by Hochreiter & Schmidhuber in 1997
    # [ Ref: http://www.bioinf.jku.at/publications/older/2604.pdf ]. 
    
    # Recurrent Neural Networks attempt to address memory issues in traditional neural networks by adding loops within them, 
    # allowing information to persist [ Ref: http://colah.github.io/posts/2015-08-Understanding-LSTMs/ ]. A resonable analogy, 
    # is to envision recurrent neural network as numerous copies of the same network, each passing a message to a parent. 
    # This chain-like nature resembles the behaviour of sequences and lists, making them naturally suited to the 
    # architecture of a neural network. Unfortunately, RNNs are burdened with the problem of hadling long-term dependencies. 
    # As the neural network grows, gaps between past relevant data grows, and the RNN model becomes unable to learn to 
    # connect the information.
    
    # In theory, RNNs are absolutely capable of handling this issue. In fact, some are. Long Short Term Memory is an extension 
    # of or type of RNN that is capable. LSTM is very efficient on a large variety of problems, including timeline data 
    # [ Ref: https://dashee87.github.io/deep%20learning/python/predicting-cryptocurrency-prices-with-deep-learning/ ], 
    # and are now widely used. LSTMs have another loop learning what data to forget and what data to remember. LSTM models 
    # still have this chain like structure, but with four different layers communicating in a certain way.
    
    # The idea to use a stacked LSTM model stemed from: https://machinelearningmastery.com/stacked-long-short-term-memory-networks/
    
    model.add(LSTM(neurons, return_sequences=True, input_shape=(inputs.shape[1], inputs.shape[2])))
    
    # Adapetd from: https://stackoverflow.com/questions/40331510/how-to-stack-multiple-lstm-in-keras
    # model.add(LSTM(neurons, return_sequences=True))
    model.add(LSTM(neurons))
    
    model.add(Dropout(dropout))
    model.add(Dense(units=output_size))
    model.add(Activation(activ_func))

    model.compile(loss=loss, optimizer=optimizer)
    return model