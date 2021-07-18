# coding=utf-8
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from sklearn.metrics import mean_squared_error
from keras.callbacks import EarlyStopping

DATA_FOLDER = r"C:\Users\dangn\OneDrive - VNU-HCMUS\HKII-2020-2021\Knowledge Representation\Stock-Market-Prediction-using-Prior-Knowledge\data"

#DATA_FILE = 'summary_data.csv'
DATA_FILE = 'summary.csv'

# Load and split data
data = pd.read_csv('{}{}{}'.format(DATA_FOLDER, os.sep, DATA_FILE))
data.drop(columns='DateTime', inplace=True)

# Split data
X, y = data.drop(columns='CloseFixed'), data['CloseFixed']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])
y_train = y_train.reshape(y_train.shape[0], 1, 1)
y_test = y_test.reshape(y_test.shape[0], 1, 1)


# LSTM MODEL
batch_size = 100
input_dim = 3
input_timesteps = 1
neurons = 50
epochs = 5
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
earlyStop=EarlyStopping(monitor="val_loss",verbose=2,mode='min',patience=3)

# Fit the model
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, 
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

plt.plot(y_train.reshape(y_train.shape[0], 1), label='Real value')
plt.plot(trainPredict.reshape(trainPredict.shape[0], 1), color='red', label='Predicted value')
plt.legend()
plt.show()

