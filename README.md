# STOCK MARKET PREDICTION USING PRIOR KNOWLDEGE

## INSTALL ENVIROMENT

```
# clone the repository
$ git clone https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge.git
$ cd Stock-Market-Prediction-using-Prior-Knowledge
$ python3 -m venv venv
$ venv\Scripts\activate.bat
$ pip install -e .
```

## DATA

Chỉ số VNIndex, thu thập từ 2000/07/28 - 2021/07/09: [link](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/blob/main/data/vnindex.csv)

Tin tức từ Cafef, 2019-12-31 - 2021-07-15: [link](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/blob/main/data/news_cafef.csv)

Tin tức từ VNExpress, 2019-12-31 - 2021-07-15:[link](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/blob/main/data/news_vnexpress.csv)

File data đã tổng hợp [link](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/blob/main/data/summary.csv)

## CODE

01. Crawler [link](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/tree/main/code/crawler)

02. Mô hình NLP 

- [link colab](https://colab.research.google.com/drive/1pXFfDavROenwtk1kD1gIxA2DQk_2NZf8)
- [file](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/tree/main/code/code/NLP_Based_on_Underthesea.ipynb)

03. Chuẩn bị dữ liệu cho LSTM [link](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/blob/main/code/data_news_summary.py)

03. ARIMA và LSTM 

- [link colab](https://colab.research.google.com/drive/1FSSipJFkYNIHwNbA9MHTGWHnjyNuiRyJ)

ARIMA [file ARIMA](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/tree/main/code/code/ARIMA.ipynb)

Mô hình LSTM [link](https://github.com/DangNguyenTranNgoc/Stock-Market-Prediction-using-Prior-Knowledge/blob/main/code/lstm_model.py)

## SLIDE

[Bài Tập Cuối Kì Time Series](https://docs.google.com/presentation/d/1SRp3ApujZQsluR6f_aZ1NF7QMw0TyhfZjqgOQ2tk9R8/edit#slide=id.ge3059aa7e2_0_794)

[Bài Tập Cuối Kì BDTT](https://docs.google.com/presentation/d/1Sq0xeNB_wyPukq9ZnRZrIA33eeDGS5PW9vmwobdJSmM/edit#slide=id.p)
