#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup


# In[4]:


from selenium import *
from urllib.request import urlopen
from urllib.parse import quote_plus
import requests
from urllib.parse import quote_plus
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
#import csv
import openpyxl


# In[6]:


def get_title():
    url = "https://www.wevity.com/?c=find&s=1&gub=1"
    page = "&gp="
    num = 1

    title_li = []

    for i in range(10):
        print("%d 페이지" % num)
        final_url = url + page + str(num)
        html = urlopen(final_url)
        soup = BeautifulSoup(html, "html.parser")
        ul = soup.find("ul", {"class": "list"})
        ullis = ul.find_all("a")

        for ulli in ullis:
            txt = ulli.get_text()
            title_li.append(txt)
        num += 1

        while "공모전명" in title_li:
            title_li.remove("공모전명")

    return title_li


# In[8]:


def get_company():
    url = "https://www.wevity.com/?c=find&s=1&gub=1"
    page = "&gp="
    num = 1

    company_li = []

    for i in range(10):
        print("%s 페이지" % num)
        final_url = url + page + str(num)
        html = urlopen(final_url).read()
        soup = BeautifulSoup(html, "html.parser")
        organs = soup.find_all("div", {"class": "organ"})

        for organ in organs:
            txt = organ.get_text()
            company_li.append(txt)
        num += 1

    while "주최사" in company_li:
        company_li.remove("주최사")

    return company_li


# In[9]:


def get_due_date():
    url = "https://www.wevity.com/?c=find&s=1&gub=1"
    page = "&gp="
    num = 1

    date = []

    for i in range(10):
        print("%s 페이지" % num)

        final_url = url + page + str(num)
        html = urlopen(final_url).read()
        soup = BeautifulSoup(html, "html.parser")

        days = soup.find_all("div", {"class": "day"})

        for day in days:
            txt = day.get_text().strip()[0:5]
            date.append(txt)
        num += 1

    while "현재현황" in date:
        date.remove("현재현황")
    return date


# In[10]:


data_dict = {"공모전명": get_title(), "주최사": get_company(), "기한": get_due_date()}


# In[15]:


db = pd.DataFrame(data_dict)
db.to_excel("공모전.xlsx",
sheet_name="공모전데이터",
na_rep='NaN',
float_format="%.2f",
header=True,
index=True,
index_label=True,
startrow=1,
startcol=1,
freeze_panes=(2, 0)
)


# In[ ]:




