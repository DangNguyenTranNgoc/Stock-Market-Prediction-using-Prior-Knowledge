# -*- coding: utf-8 -*-
"""Stock-Market-Prediction-using-Prior-Knowledge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FSSipJFkYNIHwNbA9MHTGWHnjyNuiRyJ

# STOCK MARKET PREDICTION USING PRIOR KNOWLDEGE 

### Lớp Cao học Khoa học dữ liệu khoa Toán - Tin K30 - KHTN

### Nhóm 1 
1.   Hà Minh Tuấn          - 20C29041
2.   Nguyễn Thanh Thoại    - 20C29039
3.   Trần Ngọc Đăng Nguyên - 20C29011

[Github](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge)
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
#coding: utf-8 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

# %matplotlib inline

plt.style.use('seaborn-paper')

# Define const
DATA_FOLDER = r'/content/drive/MyDrive/Data/stock-market-prediction/'

VNINDEX_FILE_CSV = os.path.abspath('{}{}vnindex.csv'.format(DATA_FOLDER, os.sep))
VNINDEX_FILE_PKL = os.path.abspath('{}{}vnindex.pkl'.format(DATA_FOLDER, os.sep))

SCORED_DATA = 'summary_data.csv'

"""## Preprocessing 'vnindex' data"""

vnindex_raw = pd.read_csv(VNINDEX_FILE_CSV)
vnindex_raw.sample(5)

# Drop not need colunms, keep date and adjust close
drop_columns = ['<Ticker>', '<OpenFixed>', '<HighFixed>', '<LowFixed>', '<Volume>', '<Open>', 
                '<High>', '<Low>', '<Close>', '<VolumeDeal>', '<VolumeFB>', '<VolumeFS>']

vnindex = vnindex_raw.drop(columns=drop_columns, axis=1)
vnindex.sample(5)

vnindex.info()

# Change name of columns ...
vnindex.rename(columns={'<DTYYYYMMDD>': 'date','<CloseFixed>': 'CloseFixed'}, inplace=True)

# ... and date column is string. So, convert it to datetime.
vnindex['date'] = pd.to_datetime(vnindex['date'], format=r'%Y%m%d')

# Check info again
vnindex.info()

"""5058 samples is too much, we just need 380 obs (equivalent to the period from 01/2019 - 07/2021)"""

vnindex = vnindex.head(380)
vnindex

"""## Plot the data"""

vnindex.plot(x='date', y='CloseFixed', xlabel='Time', ylabel='VNIndex Point', 
            title='VNIndex by time', legend=False, figsize=(16,8))

# Plot autocorrelation
from pandas.plotting import autocorrelation_plot
autocorrelation_plot(vnindex['CloseFixed'])

"""## ARIMA model

Try with default hyperparameters
"""

!pip install "statsmodels==0.11.1"

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")

# Data prepare
X = vnindex['CloseFixed']
train_size = int(len(X) * 0.8)
train, test = X[:train_size], X[train_size:len(X)]

# Convert series data to list
history = [v for v in train]
test = [v for v in test]
prediction = list()

# function plot results
def plot_evaluate(prediction, test):
    plt.plot(test, label='Real value')
    plt.plot(prediction, color='red', label='Predicted value')
    plt.legend()
    plt.show()

# ARIMA with default hyperparameters
for t in range(len(test)):
	model = ARIMA(history)
	model_fit = model.fit()
	output = model_fit.forecast()
	y = output[0]
	prediction.append(y)
	obs = test[t]
	history.append(obs)
	print('predicted={:f}, expected={:f}'.format(y, obs))

# evaluate forecasts
rmse = mean_squared_error(y_true=test, y_pred=prediction, squared=False)
print('Test RMSE: {:.3f}'.format(rmse))

# plot forecasts against actual outcomes
plot_evaluate(prediction, test)

"""### Find the suitable hyperparameters

Using grid search with:

- Autoregressive (p_values): 0, 1, 2, 4, 6, 8, 10
- Differences (d_values): 0, 1, 2
- Moving Average (q_values): 0, 1, 2
"""

def evaluate_arima_model(X, arima_order):
    train_size = int(len(X) * 0.8)
    train, test = X[:train_size], X[train_size:]
    
    history = [v for v in train]
    test = [v for v in test]

    prediction = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit()
        y = model_fit.forecast()[0]
        prediction.append(y)
        history.append(test[t])

    rmse = mean_squared_error(test, prediction, squared=False)
    
    return rmse

def evaluate_models(dataset, p_values, d_values, q_values):
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
                try:
                    rmse = evaluate_arima_model(dataset, order)
                    print('Order: {} / RMSE: {}'.format(order, rmse))
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                        print('ARIMA%s RMSE=%.3f' % (order,rmse))
                except Exception as ex:
                    print(ex)
                    continue
    
    print('Best ARIMA{} RMSE={:.3f}'.format(best_cfg, best_score))

"""Find the suitable hyperparameters"""

# p_values = [0, 1, 2, 4, 6, 8]
# d_values = range(0, 3)
# q_values = range(0, 3)
# warnings.filterwarnings("ignore")
# evaluate_models(vnindex['CloseFixed'], p_values, d_values, q_values)

"""### Check the result"""

X = vnindex['CloseFixed']
train_size = int(len(X) * 0.7)
train, test = X[:train_size], X[train_size:len(X)]

# Convert series to list
history = [v for v in train]
test = [v for v in test]
prediction = list()

# ARIMA
for t in range(len(test)):
	model = ARIMA(history, order=(6, 2, 1))
	model_fit = model.fit()
	output = model_fit.forecast()
	y = output[0]
	prediction.append(y)
	obs = test[t]
	history.append(obs)

# evaluate forecasts
rmse = mean_squared_error(y_true=test, y_pred=prediction, squared=False)
print('Test RMSE: {:.3f}'.format(rmse))

# plot forecasts against actual outcomes
plot_evaluate(prediction, test)

pred_df = vnindex.copy()
pred_df.drop(columns='CloseFixed', inplace=True)
pred_df['CloseFixed'] = history
pred_df
pred_df.to_csv('{}{}arima_pred.csv'.format(DATA_FOLDER, os.sep), index=False)

"""## MÔ HÌNH LSTM"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from keras.callbacks import EarlyStopping

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
data = pd.read_csv('{}{}{}'.format(DATA_FOLDER, os.sep, 'summary.csv'))
data.drop(columns='DateTime', inplace=True)

# Split data
X, y = data.drop(columns='CloseFixed'), data['CloseFixed']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = preprocessing_data(X_train, is_X=True)
X_test = preprocessing_data(X_test, is_X=True)
y_train = preprocessing_data(y_train)
y_test = preprocessing_data(y_test)

# LSTM hyperparameter
batch_size = 100
input_dim = 3
input_timesteps = 1
neurons = 50
epochs = 100
dense_output = 1
drop_out = 0

# LSTM MODEL
model = Sequential()
model.add(LSTM(neurons, input_shape=(1, input_dim), return_sequences=True))
model.add(Dropout(drop_out))
model.add(LSTM(neurons,return_sequences = True))
model.add(LSTM(neurons,return_sequences = False))
model.add(Dropout(drop_out))
model.add(Dense(dense_output, activation='linear'))

# Compile model
model.compile(loss='mean_squared_error',
                optimizer='adam')
earlyStop=EarlyStopping(monitor="val_loss",verbose=2,mode='min',patience=3)

# Fit the model
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), callbacks=[earlyStop])

print(model.summary())

# make predictions
trainPredict = model.predict(X_train)
testPredict = model.predict(X_test)

# calculate root mean squared error
trainScore = mean_squared_error(y_train[0], trainPredict[0], squared=False)
print('Train Score: %.2f RMSE' % (trainScore))
testScore = mean_squared_error(y_test[0], testPredict[0], squared=False)
print('Test Score: %.2f RMSE' % (testScore))

fig, (ax1, ax2) = plt.subplots(2, figsize=(16,8))

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