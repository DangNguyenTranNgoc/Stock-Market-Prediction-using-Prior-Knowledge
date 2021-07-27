# coding=utf-8
import os
import pandas as pd

DATA_FOLDER = r"C:\Users\dangn\OneDrive - VNU-HCMUS\HKII-2020-2021\Knowledge Representation\Stock-Market-Prediction-using-Prior-Knowledge\data"

VNINDEX_PRED_FILE = 'arima_pred.csv'
VNINDEX_FILE = 'vnindex.pkl'

# News files
CAFEF_FILE = 'news_cafef_scored.csv'
VNEXPRESS_FILE = 'news_vnexpress_scored.csv'

def remove_unnessessary(data: pd.DataFrame):
    '''
    Remove weekend from DataFrame
    Ex: if df.iloc[0]['DateTime'].weekday() > 5:
            df.drop(index)
    '''
    data.drop(columns=['Title','ShortContent'], inplace=True)
    data['DateTime'] = pd.to_datetime(data['DateTime']).dt.date
    for index, row in data.iterrows():
        if row['DateTime'].weekday() >= 5:
            data.drop(index, inplace=True)

def summary_sentiment_score(data: pd.DataFrame, name: str):
    '''
    '''
    df = data.groupby(['DateTime'], as_index=False) \
           .apply(lambda d: d['Sentiment'].sum() / d['Sentiment'].count())

    df.columns = ['DateTime', name]
    return df

def main():
    '''
    Convert cafef datetime to date.
    Ex: groupby(['DateTime']).sum()
    call other function to summary by date per data
    '''
    # Load data
    cafef_df = pd.read_csv('{}{}{}'.format(DATA_FOLDER, os.sep, CAFEF_FILE), index_col=0)
    vnexpress_df = pd.read_csv('{}{}{}'.format(DATA_FOLDER, os.sep, VNEXPRESS_FILE), index_col=0)

    # Remove weekend from news
    remove_unnessessary(cafef_df)
    remove_unnessessary(vnexpress_df)

    # Sum the sentiments score by day
    cafef_df = summary_sentiment_score(cafef_df, 'cafef')
    vnexpress_df = summary_sentiment_score(vnexpress_df, 'vnexpress')

    # Merge two news data
    summary_df = cafef_df.merge(vnexpress_df)

    # Load and correct vnindex ARIMA predicted data
    vnindex_pred_df = pd.read_csv('{}{}{}'.format(DATA_FOLDER, os.sep, VNINDEX_PRED_FILE))
    vnindex_pred_df.rename(columns={'date':'DateTime', 'CloseFixed':'Predicted'}, inplace=True)
    vnindex_pred_df['DateTime'] = pd.to_datetime(vnindex_pred_df['DateTime']).dt.date

    # Merge vnindex data to current data
    summary_df = summary_df.merge(vnindex_pred_df, on='DateTime', how='inner')

    # Load and correct vnindex data
    vnindex_df = pd.read_pickle('{}{}{}'.format(DATA_FOLDER, os.sep, VNINDEX_FILE))
    vnindex_df.rename(columns={'date':'DateTime'}, inplace=True)
    vnindex_df['DateTime'] = pd.to_datetime(vnindex_df['DateTime']).dt.date

    summary_df = summary_df.merge(vnindex_df, on='DateTime', how='inner')

    # Export to csv
    summary_df.to_csv('{}{}summary.csv'.format(DATA_FOLDER, os.sep), index=False)


if __name__ == '__main__':
    main()
