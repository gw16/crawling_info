from django.shortcuts import render
from .models import Thinkyou
import pymysql

# Create your views here.

connection = pymysql.connect(host='localhost', port=3306, user='root', password='x03md2$9c', db='craw_table',
                             charset='utf8', autocommit=True)
cursor = connection.cursor()
query_string = "select 제목, 공지일, 마감일, 날짜, 기관, 링크 from thinkyou"
cursor.execute(query_string)
rows = cursor.fetchall()
dicts = []

for row in rows:
    dic = {'제목': row[0], '공지일': row[1], '마감일': row[2], '날짜': row[3], '기관': row[4], '링크': row[5]}
    dicts.append(dic)


def index(request):
    posts = dicts
    return render(request, 'crawled_data/index.html', {"posts": posts})
