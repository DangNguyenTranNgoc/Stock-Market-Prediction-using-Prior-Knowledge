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

"""### Save the predicted score """
pred_df = vnindex.copy()
pred_df.drop(columns='CloseFixed', inplace=True)
pred_df['CloseFixed'] = history
pred_df
pred_df.to_csv('{}{}arima_pred.csv'.format(DATA_FOLDER, os.sep), index=False)
