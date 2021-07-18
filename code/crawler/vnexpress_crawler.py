# coding=utf-8
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import re

START_PAGE = "https://vnexpress.net/"
PAGE_NUMBERS = range(1, 45)
DATA_FOLDER = r'C:\Users\dangn\OneDrive - VNU-HCMUS\HKII-2020-2021\Knowledge Representation\Stock-Market-Prediction-using-Prior-Knowledge\data'

def parse_list_page():
    data = pd.DataFrame(columns=['DateTime', 'Title', 'ShortContent'])
    
    for page in PAGE_NUMBERS:
        link = '{}kinh-doanh/chung-khoan-p{}'.format(START_PAGE, page)
        print("========================================")
        print('Parsing page {}'.format(link))
        print("========================================")
        news = parse_detail_page(link)
        data = data.append(news)

    return data

def parse_detail_page(url):
    '''
    items[6].ins is exist => next
    title: items[0].h2.text
    description: items[0].p.text
    get link article: items[0].h2.a.attrs['href']
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    items = soup.find_all('article')
    news = pd.DataFrame(columns=['DateTime', 'Title', 'ShortContent'])

    for item in items:
        try:
            if item.ins:
                continue

            article_url = item.h2.a.attrs['href']
            print("Article: {}".format(article_url))
            date = get_datetime_from_page(article_url)
            title = item.h2.text.strip()
            short_content = item.p.text.strip()
            news = news.append({'DateTime' : date, 
                            'Title' : title, 
                            'ShortContent' : short_content},
                            ignore_index=True)

        except Exception as ex:
            print(ex.__cause__)
            pass
                        
    return news


def get_datetime_from_page(url: str) -> str:
    '''
    Get date from an article
    ===
    date = ssoup.find('span', {'class':'date'})
    date.text => 'Thứ năm, 15/7/2021, 16:58 (GMT+7)'
    ===
    return date or None
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    date = soup.find('span', {'class':'date'})

    return parse_date(date.text)

def parse_date(str: str) -> str:
    '''
    Parse date from string
    ===
    Ex: 'Thứ năm, 15/7/2021, 16:58 (GMT+7)' => 15/7/2021 
    '''
    pattern = r'(?<=,)(.*?)(?=,)'
    date = re.search(pattern, str)
    if date:
        return date[0].strip()
    
    return None

def main():
    """
    Push callback method and url to queue
    """
    vnexpress_df = parse_list_page()
    vnexpress_df['DateTime'] = pd.to_datetime(vnexpress_df['DateTime'], format=r'%d/%m/%Y')
    vnexpress_df.reset_index(drop=True, inplace=True)
    vnexpress_df.to_csv('{}{}news_vnexpress.csv'.format(DATA_FOLDER, os.sep), encoding='utf-8')

if __name__ == '__main__':
    main()



