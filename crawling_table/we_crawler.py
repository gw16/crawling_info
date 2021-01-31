import pandas as pd
import numpy as np
import csv
import os

#크롤링을 위한 라이브러리
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from urllib.parse import urlparse
import time
from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "crawling_table.settings")
import django
django.setup()
from crawled_data.models import BoardData




url_base ='https://www.wevity.com/?c=find&s=1&gub=1&cidx=21'
headers = {'User-Agent':'Mozilla/5.0'} 
res = requests.get(url_base, headers=headers)
soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')

links = []
titles = []
day_list = []
dday = []
cite_type = []
inst = []
dates = []
k=1

def fetch_we_latest_data(page_num):
    k=1
    result = []
    while k<=page_num :
        # 페이지 수 2까지
        url= 'https://www.wevity.com/?c=find&s=1&gub=1&cidx=21&gp='+ str(k) 

        base_url = 'https://www.wevity.com/'
        headers = {'User-Agent':'Mozilla/5.0'} 
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
        
        len_link = len(soup.select('li > .tit > a'))
        print(len_link)
        for i in range(len_link):
            titles.append(soup.select('.tit > a')[i].text)
            links.append(base_url + soup.select('li > .tit > a')[i]['href'])
            cite_type.append(soup.select('.tit >.sub-tit')[i].text)

        k+=1


        table_data = {'title': titles,
                    'link':links,
                    'specific_id': cite_type}

        BoardData(specific_id=cite_type,
                    title=titles,
                    link=links).save()


    result.append(table_data)
    return result    
   # return table_data




if __name__ == '__main__':
    print(fetch_we_latest_data(2))




