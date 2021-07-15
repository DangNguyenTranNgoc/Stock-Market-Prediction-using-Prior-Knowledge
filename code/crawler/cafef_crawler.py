# coding=utf-8
'''
Defind structure of data:
cafef_news = {
    'YYYYMMDDhhmmss' : {
        'title' : 'string',
        'short_content' : 'string'
    }
}
'''
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import os

START_PAGE = "https://cafef.vn/timeline/31/"
PAGE_NUMBERS = range(1, 750)
DATA_FOLDER = r'C:\Users\dangn\OneDrive - VNU-HCMUS\HKII-2020-2021\Knowledge Representation\Stock-Market-Prediction-using-Prior-Knowledge\data'

def parse_list_page():
    data = pd.DataFrame(columns=['DateTime', 'Title', 'ShortContent'])
    
    for page in PAGE_NUMBERS:
        link = '{}trang-{}.chn'.format(START_PAGE, page)
        print('Parsing page {}'.format(link))
        news = parse_detail_page(link)
        data = data.append(news)

    return data

def parse_detail_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    items = soup.find_all('li')
    news = pd.DataFrame(columns=['DateTime', 'Title', 'ShortContent'])
    
    for item in items:
        try:
            date = item.attrs['data-newsid'][:-3]
            title = item.h3.text
            short_content = item.find('p', {'class':'sapo'}).text
            news = news.append({'DateTime' : date, 
                            'Title' : title, 
                            'ShortContent' : short_content},
                            ignore_index=True)
        except Exception as ex:
            print(ex.__cause__)
            pass
                        
    return news

def main():
    """
    Push callback method and url to queue
    """
    cafef_df = parse_list_page()
    cafef_df['DateTime'] = pd.to_datetime(cafef_df['DateTime'], format=r'%Y%m%d%H%M%S')
    cafef_df.reset_index(drop=True, inplace=True)
    cafef_df.to_csv('{}{}news_cafef.csv'.format(DATA_FOLDER, os.sep), encoding='utf-8')

if __name__ == '__main__':
    main()


