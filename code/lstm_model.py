# coding=utf-8
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from keras.callbacks import EarlyStopping

DATA_FOLDER = r"C:\Users\dangn\OneDrive - VNU-HCMUS\HKII-2020-2021\Knowledge Representation\Stock-Market-Prediction-using-Prior-Knowledge\data"

DATA_FILE = 'summary.csv'

def preprocessing_data(data, is_X=None):
    '''
    Preprocessing data before put it to model:
    - Reshape data
    - Min max scale data
    '''
    _data = data
    _data = _data.to_numpy()
    min_max_scaler = MinMaxScaler()
    
    if is_X:
        _data[[2]] = min_max_scaler.fit_transform(_data[[2]])

    if len(_data.shape) == 1:
        _data = _data.reshape(_data.shape[0], 1)
        _data = min_max_scaler.fit_transform(_data)
    
    _data = _data.reshape(_data.shape[0], 1, _data.shape[1])

    return _data

# Load and split data
data = pd.read_csv('{}{}{}'.format(DATA_FOLDER, os.sep, DATA_FILE))
data.drop(columns='DateTime', inplace=True)

# Split data
X, y = data.drop(columns='CloseFixed'), data['CloseFixed']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = preprocessing_data(X_train, is_X=True)
X_test = preprocessing_data(X_test, is_X=True)
y_train = preprocessing_data(y_train)
y_test = preprocessing_data(y_test)

# LSTM MODEL
batch_size = 100
input_dim = 3
input_timesteps = 1
neurons = 50
epochs = 100
dense_output = 1
drop_out = 0

model = Sequential()
model.add(LSTM(neurons, input_shape=(1, input_dim), return_sequences=True))
model.add(Dropout(drop_out))
model.add(LSTM(neurons,return_sequences = True))
model.add(LSTM(neurons,return_sequences =False))
model.add(Dropout(drop_out))
model.add(Dense(dense_output, activation='linear'))

# Compile model
model.compile(loss='mean_squared_error',
                optimizer='adam')
earlyStop = EarlyStopping(monitor="val_loss", verbose=2, mode='min', patience=3)

# Fit the model
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, 
          validation_data=(X_test, y_test), callbacks=[earlyStop])
print(model.summary())

# make predictions
trainPredict = model.predict(X_train)
testPredict = model.predict(X_test)

# calculate root mean squared error
trainScore = mean_squared_error(y_train[0], trainPredict[0], squared=False)
print('Train Score: %.2f RMSE' % (trainScore))
testScore = mean_squared_error(y_test[0], testPredict[0], squared=False)
print('Test Score: %.2f RMSE' % (testScore))

fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(history.history['loss'])
ax1.plot(history.history['val_loss'])
ax1.set_title('Model loss')
ax1.set_ylabel('Loss')
ax1.set_xlabel('Epoch')
ax1.legend(['Train', 'Test'])

ax2.plot(y_train.reshape(y_train.shape[0], 1))
ax2.plot(trainPredict.reshape(trainPredict.shape[0], 1))
ax2.set_title('Train predicted')
ax2.set_ylabel('Real value')
ax2.set_xlabel('Predicted value')
ax2.legend(['Train', 'Predict'])

plt.show()
