import pandas as pd
import numpy as np
import csv

#크롤링을 위한 라이브러리
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import time
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import mysql.connector

import schedule
import time
from datetime import datetime


def browser():

    url ='https://thinkyou.co.kr/contest/sector.asp'

    browser = Chrome(r"C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe")

    delay=3
    browser.implicitly_wait(delay)

    browser.get(url)

    browser.maximize_window()

    body = browser.find_element_by_tag_name('body')

    try :

        browser.find_elements_by_xpath('//*[@id="searchFrm"]/div/dl[1]/dd/p[6]/label/span')[0].click()
        browser.find_elements_by_xpath('//*[@id="searchFrm"]/div/dl[2]/dd/p[1]/label/span')[0].click()
    except:
        pass

    SCROLL_PAUSE_TIME = 0.5
    while True:
        last_height = browser.execute_script('return document.documentElement.scrollHeight')

        for i in range(3):
            body.send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            break;

    page = browser.page_source
    soup = BeautifulSoup(page, 'lxml')
    return soup


def crawling():
    soup = browser()

    len_day = 20

    links_bef = []
    titles_bef = []
    dday_bef = []
    inst_bef = []
    start_bef = []
    end_bef = []

    links_aft = []
    titles_aft = []
    inst_aft = []

    for i in range(len_day):
        t = soup.select(' .title > a > dl > dt ')[i].text
        fin = soup.select(' .statNew > p ')[i].text


        if fin == '마감':
            base_url = 'https://thinkyou.co.kr'
            titles_aft.append(soup.select(' .title > a > dl > dt ')[i].text)
            inst_aft.append(soup.select(' .title > a > dl > dd ')[i].text.split(':')[1][1:])

            links_aft.append(base_url + soup.select(' .title > a')[i]['href'][2:])
        else:
            stand = soup.select(' .statNew')[i].text.split('D')[1]


            if stand == '-day':
                base_url = 'https://thinkyou.co.kr'
                titles_bef.append(soup.select(' .title > a > dl > dt ')[i].text)
                inst_bef.append(soup.select(' .title > a > dl > dd ')[i].text.split(':')[1][1:])
                dday_bef.append('D' + soup.select(' .statNew')[i].text.split('D')[1])
                links_bef.append(base_url + soup.select(' .title > a')[i]['href'][2:])
                a = i * 2
                start_bef.append(soup.select(' .etc')[a].text[:8])
                end_bef.append(soup.select(' .etc')[a].text[11:])

            else:

                base_url = 'https://thinkyou.co.kr'
                titles_bef.append(soup.select(' .title > a > dl > dt ')[i].text)
                inst_bef.append(soup.select(' .title > a > dl > dd ')[i].text.split(':')[1][1:])
                dday_bef.append('D' + soup.select(' .statNew')[i].text.split('D')[1])
                links_bef.append(base_url + soup.select(' .title > a')[i]['href'][2:])
                a = i * 2
                start_bef.append(soup.select(' .etc')[a].text[:8])
                end_bef.append(soup.select(' .etc')[a].text[11:])

    tabl_data_bef = {'제목': titles_bef, '공지일': start_bef, '마감일': end_bef, '날짜': dday_bef, '기관': inst_bef,
                     '링크': links_bef}
    df_bef = pd.DataFrame(tabl_data_bef, columns=['제목', '공지일', '마감일', '날짜', '기관', '링크'])


    tabl_data_aft = {'제목': titles_aft, '기관': inst_aft, '링크': links_aft}
    df_aft = pd.DataFrame(tabl_data_aft, columns=['제목', '날짜', '링크'])

    return df_bef


def tosql():
    df = crawling()
    engine = create_engine("mysql+pymysql://root:x03md2$9c@LOCALhost:3306/CRAW_TABLE", encoding='utf-8', echo=False)

    df.to_sql(name='thinkyou', con=engine, if_exists='replace', index=False)


def job():
    now = datetime.now()
    print(now)
    tosql()


schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
