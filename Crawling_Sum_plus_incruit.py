#!/usr/bin/env python
# coding: utf-8

# In[1]:


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd


# In[2]:


import numpy as np
import csv

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


import schedule
import time
from datetime import datetime


# In[3]:


import pyrebase


# In[37]:


def browser():

    url ='https://thinkyou.co.kr/contest/sector.asp'

    browser = Chrome('/Users/gareth/chromedriver')

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


# In[38]:


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
                num = 0
                base_url = 'https://thinkyou.co.kr'
                titles_bef.append(soup.select(' .title > a > dl > dt ')[i].text)
                inst_bef.append(soup.select(' .title > a > dl > dd ')[i].text.split(':')[1][1:])
                dday_bef.append(num)
                links_bef.append(base_url + soup.select(' .title > a')[i]['href'][2:])
                a = i * 2
                start_bef.append(soup.select(' .etc')[a].text[:8])
                end_bef.append(soup.select(' .etc')[a].text[11:])

            else:

                base_url = 'https://thinkyou.co.kr'
                titles_bef.append(soup.select(' .title > a > dl > dt ')[i].text)
                inst_bef.append(soup.select(' .title > a > dl > dd ')[i].text.split(':')[1][1:])
                dday_bef.append(soup.select(' .statNew')[i].text.split('-')[1])
                links_bef.append(base_url + soup.select(' .title > a')[i]['href'][2:])
                a = i * 2
                start_bef.append(soup.select(' .etc')[a].text[:8])
                end_bef.append(soup.select(' .etc')[a].text[11:])
                
    print(inst_bef)

    tabl_data_bef = {'title': titles_bef, 'notice': start_bef, 'deadline': end_bef, 
                     'dday': dday_bef, 'sponsor': inst_bef, 'title2': titles_bef, 'link': links_bef}
    print(tabl_data_bef)

    df_bef = pd.DataFrame(tabl_data_bef, columns=['type', 'qualification', 'title', 
                                                  'notice', 'deadline', 'dday', 'sponsor', 'title2', 'link'])
    
    df_bef['type'] = '공모전'
    df_bef['qualification'] = '대학(원)생'


    return df_bef


# In[39]:


def browser2():
    url_base = 'https://www.thinkcontest.com/Contest/CateField.html?page=1&c=11'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url_base, headers=headers)
    soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
    key = ['과학/공학', '게임/소프트웨어']
    links = []
    titles = []
    dday = []
    inst = []
    dates = []
    k = 1
    
    while k <= 10:
        url = 'https://www.thinkcontest.com/Contest/CateField.html?page=' + str(k) + '&c=11'
        base_url = 'https://www.thinkcontest.com/'
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
        len_link = len(soup.select(' .txt-left > .contest-title > a'))
        for i in range(len_link):
            if soup.select(' td > span ')[i].text.replace('\n', '') == '마감':
                break
            else:
                titles.append(soup.select(' .txt-left > .contest-title > a')[i].text)
                links.append(base_url + soup.select('.txt-left > .contest-title > a ')[i]['href'])
                dday.append(soup.select(' td > p ')[i].text.split('-')[1])
        k=k+1
                            
    str_date = []
    end_date = []
    participate = []
    for i in range(len(links)):
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(links[i], headers=headers)
        soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
        html = soup.select(' tr')
        text = str(html).replace('\n', '')
        certi = re.compile('참가자격' + '.{200}')
        test = certi.findall(text)[0]
        partis = []
        if '대학생' in test:
            partis.append('대학생')
        else:
            pass

        if '대학원생' in test:
            partis.append('대학원생')
        else:
            pass

        if '일반인' in test:
            partis.append('일반인')
        else:
            pass

        if '국내외 석학과 연구진' in test:
            partis.append('국내외 석학과 연구진')
        else:
            pass

        if '제한없음' in test:
            partis.append('제한없음')
        else:
            pass

        if '어린이' in test:
            partis.append('어린이')
        else:
            pass

        if '초등학생' in test:
            partis.append('초등학생')
        else:
            pass

        if '중학생' in test:
            partis.append('중학생')
        else:
            pass

        if '고등학생' in test:
            partis.append('고등학생')
        else:
            pass
        participant = str(partis).replace('[', '').replace(']', '').replace("'", "")
        start = re.compile('접수기간' + '.{19}')
        strdate = start.findall(text)[0].split('<td>')[1]
        end = re.compile('접수기간' + '.{32}')
        enddate = end.findall(text)[0].split('~')[1].replace(' ', '')
        participate.append(participant)
        str_date.append(strdate)
        end_date.append(enddate)
        inst.append(soup.select(' tbody > tr > td ')[0].text)
        
        

    tabl_data = {'title': titles, 'notice': str_date, 'deadline': end_date, 'dday': dday,
                 'qualification': participate, 'sponsor': inst, 'title2': titles,'link': links}

    df2 = pd.DataFrame(tabl_data, columns=['type', 'qualification', 'title', 
                                           'notice', 'deadline', 'dday', 'sponsor', 'title2', 'link'])
    df2['type'] = '공모전'

    return df2


# In[40]:


def days_dreams():
    dday_bef = []
    page_num = 1
    while(page_num <=5):        
        url = 'https://www.dreamspon.com/scholarship/scholarship02.html?page=' + str(page_num)
        req = urllib.request.urlopen(url)
        res = req.read()
        soup = BeautifulSoup(res,'html.parser')
        days = soup.select(" .td_day > .count")        
        for i in range(len(days)):
            if 'D+' in str(days[i].text):
                pass
            else:
                
                dday_bef.append((days[i].text).strip("D-"))
        page_num += 1  
    return dday_bef


# In[41]:


def link_test_dreams():
    link_test = []
    page_num = 1
    while(page_num <=5):        
        url = 'https://www.dreamspon.com/scholarship/scholarship02.html?page=' + str(page_num)
        req = urllib.request.urlopen(url)
        res = req.read()
        soup = BeautifulSoup(res,'html.parser')
        contests = soup.find_all("p",class_="title")
        days = soup.select(" .td_day > .count")        
        for i in range(len(days)):
            if 'D+' in str(days[i].text):
                pass
            else:
                link_test.append(str(contests[i]).strip('[<p class="title"><a href="').strip('</a>'))
        page_num += 1  
    return link_test


# In[42]:


def link_dreams(link_test):
    link_bef=[]
    page_num = 1
    for t in range(len(link_test)):
        link_address, title_name = link_test[t].split('">')
        link_ver1 = "https://www.dreamspon.com/" + link_address
        link_bef.append(link_ver1)
    page_num += 1  
    return link_bef


# In[43]:


def titles_dreams(link_test):
    titles_bef = [] # 행사 이름
    page_num = 1
    for t in range(len(link_test)):
        link_address, title_name = link_test[t].split('">')
        titles_bef.append(title_name)
    page_num += 1  
    return titles_bef


# In[44]:


def insts_dreams():
    inst = []
    page_num = 1
    while(page_num <=5):
        url = 'https://www.dreamspon.com/scholarship/scholarship02.html?page=' + str(page_num)
        req = urllib.request.urlopen(url)
        res = req.read()
        soup = BeautifulSoup(res,'html.parser')
        idx = 1
        while(idx<=60):
            if 'D-' in str(soup.select("tr>td")[idx+1].text):
                inst.append(soup.select("tr>td")[idx].text) #       1,5,9, 13
            idx += 4    
        page_num += 1
    return inst


# In[45]:


def s_e_test_dreams(list_adress):

    driver = webdriver.Chrome('/Users/gareth/chromedriver')
    driver.implicitly_wait(10)
    login_path ='//*[@id="loginForm"]/div[1]/input'

    driver.get("https://www.dreamspon.com/" + list_adress)
    result = driver.switch_to_alert()
    result.accept()

    driver.find_element_by_name('mbr_id').send_keys('rainrain16@hanmail.net')
    driver.find_element_by_name('pwd_in').send_keys('rainrain16')
    driver.find_element_by_xpath(login_path).click()
    #   response = driver.get("https://www.dreamspon.com/" + link_adress)
    sleep(2)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')



    crawl_data =soup.select("dl >dd >p>b")[0].text


    start_day, end_day  = (crawl_data).split('~')



    return start_day, end_day


# In[46]:


def s_e_test_dreams(list_adress):

    driver = webdriver.Chrome('/Users/gareth/chromedriver')
    driver.implicitly_wait(10)
    login_path ='//*[@id="loginForm"]/div[1]/input'

    driver.get(list_adress)
    result = driver.switch_to_alert()
    result.accept()

    driver.find_element_by_name('mbr_id').send_keys('rainrain16@hanmail.net')
    driver.find_element_by_name('pwd_in').send_keys('rainrain16')
    driver.find_element_by_xpath(login_path).click()
    #   response = driver.get("https://www.dreamspon.com/" + link_adress)
    sleep(1)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')



    crawl_data = str(soup.find_all("li", class_= "day"))
#    crawl_data = (crawl_data.strip('[<li class="day" style="height: 70px; ">')).strip('\n\t')


#    start_day, end_day_ver1  = (crawl_data).split('~')
#    end_day_ver2, end_day_ver3 =  (end_day_ver1).split("<span>D")
    
#    return start_day, end_day_ver1

    
    return crawl_data


# In[47]:


def s_e_days_dreams():
    crawl=[]
    sd_days_list = link_dreams(link_test_dreams())
    
    for i in range(len(sd_days_list)):
        crawl.append(s_e_test_dreams(sd_days_list[i]))
    return crawl


# In[48]:


def s_e_preprocess():
    s_e_pre = s_e_days_dreams()
    
    for i in range(len(s_e_pre)):
        s_e_pre[i] = (s_e_pre[i].strip('[<li class="day" style="height: 70px; ">')).strip('\n\t')
#         start_day, end_day_ver1  = (crawl_data).split('~')
#         end_day_ver2, end_day_ver3 =  (end_day_ver1).split("<span>D")
    
#    return start_day, end_day_ver1
    return s_e_pre


# In[49]:


def s_e_final():
    s_e_pre = s_e_preprocess()
    start_bef = []
    end_bef = []
    for i in range(len(s_e_pre)):
        if '(1차)' not in s_e_pre[i]:
            start_day, end_day_ver1  = (s_e_pre[i]).split('~')
            end_day_ver2, end_day_ver3 =  (end_day_ver1).split("<span>D")
            start_bef.append(start_day)
            end_bef.append(end_day_ver2)

        else:            
            start_ver1, start_ver2 = (s_e_pre[i]).split('</span><br/>')
            start_ver3, end_ver1 = start_ver1.split('~')
            end_ver2, end_ver3 = end_ver1.split('<span')

            start_ver4 ,end_ver4  = start_ver2.split('~')

            
            end_ver5, end_ver6 = end_ver4.split('<span')

            
            start_bef.append(start_ver3 + "& " + start_ver4)
            end_bef.append("(1차 마감일)"+end_ver2+"& "+"(2차 마감일)"+end_ver5)

#    print(len(start_bef),len(end_bef))
    return start_bef, end_bef


# In[50]:


def final_dreams():
    dday =  days_dreams()
    links = link_dreams(link_test_dreams())
    title = titles_dreams(link_test_dreams())
    start, end = s_e_final()
    inst = insts_dreams()

#     tabl_data_bef = {'title': title, 'notice': start,  'deadline': end, 'dday': dday, 'sponsor': inst, 'title2': title,
#                      'link': links}
#     df_bef = pd.DataFrame(tabl_data_bef, columns=['title', 'notice', 'deadline', 'dday', 'sponsor', 'title2', 'link'])
#     df_bef['type'] = '장학금'
#     df_bef['qualification'] = '대학생'
    
    tabl_data_bef = {'type':"장학금", 'qualification': "대학생",'title': title, 'notice': start,  'deadline': end, 'dday':dday, 'sponsor':inst, 'title2': title,
                     'link':links}
#     df_bef = pd.DataFrame()
#     df_bef['type'] = '공모전'
#     df_bef['qualification'] = '대학(원)생'
    df_bef = pd.DataFrame(tabl_data_bef, columns=['type', 'qualification', 'title', 'notice', 'deadline', 'dday', 'sponsor', 'title2', 'link'])




    return df_bef


# In[11]:


def incruit():
    url='https://gongmo.incruit.com/list/gongmolist.asp?ct=1&category=11'
    req=urllib.request.urlopen(url)
    res=req.read()
    soup=BeautifulSoup(res,'html.parser')
    data_list = soup.find(id='tbdyGmScrap').find_all('a')
    for data in data_list:
        req = requests.get(data.get('href'))
        soup = BeautifulSoup(req.content, "html.parser")
        tmp = soup.find(class_='tBrd1Gray').find_all('td')
        title = soup.find(class_='job_new_top_title').get_text()
        term = tmp[3].get_text()
        classify = tmp[0].get_text().replace("<br/>", ",")
        host = tmp[1].get_text()
        link = tmp[4].find('a').get('href').replace('\t', '')
        contest_in= [title, term, classify, host, link]

        start_bef, end_bef=term.split('~')


# In[12]:


data=pd.DataFrame(contests)
data1=data.transpose()
del data1[2]
data1.loc[:,'notice'] = [start_bef]
data1.loc[:,'deadline']=[end_bef]
del data1[1]
data2['type']='공모전'
data2['Qualification']='대학(원)생'
data2['title2']=data2['title']
today=datetime.date.today()
targetday=datetime.date(2021,10,4)
delta=targetday-today
data2['dday']=delta.days


# In[13]:


def tofb():
    df1 = crawling()
    df2 =  final_dreams()
    df3 = browser2()
    df4 = data2

    mid = pd.concat([df1, df2,df3,df4]) 
    mid_df = mid.reset_index(drop=True)
    mid_df['title'] = mid_df['title'].str.strip()
    fin_df = mid_df.drop_duplicates(['title'], keep='first')
    fin = fin_df.reset_index(drop = True)
    

    postdata = fin.to_dict(orient="index")
    config = {
        "apiKey": "AIzaSyDIo8bt7OrCX6KYaxplvUauQdaehcjUo_0",
        "authDomain": "activity-crawling.firebaseapp.com",
        "databaseURL": "https://activity-crawling-default-rtdb.firebaseio.com",
        "projectId": "activity-crawling",
        "storageBucket": "activity-crawling.appspot.com",
        "messagingSenderId": "608978503357",
        "appId": "1:608978503357:web:374a269b8fa1a64888d9d4"}
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child().update(postdata)


# In[14]:


tofb()


# In[ ]:




