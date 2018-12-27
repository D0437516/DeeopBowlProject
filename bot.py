import json
import parser
import sys
import pymysql
import pandas as pd
import flask as Flask
from datetime import datetime
from dateutil import parser

def OpenDB():
    db = pymysql.connect(
        user = 'root',
        password = '0604',
        database = 'project',
        charset = 'utf8'
    )
    return db

def SearchDB(sql):
    conn = OpenDB()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def getstring(inf):
    information = []
    for i in inf:
        for j in i:
            information.append(str(j))
    for i in information:
        print(i,type(i))
    strinfo =' \n'.join(information)
    return strinfo

def msg(inf):
    print(inf)
    return inf

#球電影資訊
def find_movie_information(keyword):
    sql = 'SELECT Cname FROM movie, movie_actor, movie_director, movie_type WHERE  Cname = \'' + keyword + '\' AND MNum = A AND MNum = D AND MNum = Tnum'
    inf = SearchDB(sql)
    inf_1 = getstring(inf)
    msg(inf_1)
    return inf_1
#求電影上映時間
def find_movie_date(start,end):
    if end != None:
        sql = 'SELECT Cname FROM movie WHERE  Date >=\'' + start.strftime('%Y/%m/%d') + '\' AND Date <= \'' + end.strftime('%Y/%m/%d') + '\''
        inf = SearchDB(sql)
        inf_1 = getstring(inf)

    elif start != None:
        sql = 'SELECT Cname FROM movie WHERE  Date = \'' + start .strftime('%Y/%m/%d')+ '\''
        inf = SearchDB(sql)
        inf_1 = getstring(inf)
    else:
        today = datetime.today().date()
        sql = 'SELECT Cname FROM movie WHERE  Date = \'' + today .strftime('%Y/%m/%d')+ '\''
        inf = SearchDB(sql)
        inf_1 = getstring(inf)
    msg(inf_1)
    return inf_1
#求演員演過的電影
def find_movie_actor(keyword):
    sql = 'SELECT Cname FROM movie, movie_actor WHERE  Actor = \'' + keyword + '\' AND MNum = Anum '
    inf = SearchDB(sql)
    inf_1 = getstring(inf)
    msg(inf_1)
    return inf_1
#求類型電影
def find_movie_category(keyword):
    sql = 'SELECT Cname FROM movie, movie_type WHERE  Type = \'' + keyword + '\' AND MNum = Tnum '
    inf = SearchDB(sql)
    inf_1 = getstring(inf)
    msg(inf_1)
    return inf_1
#關鍵字找電影
def find_movie(keyword):
    sql = 'SELECT Cname FROM movie WHERE  Content LIKE \'%' + keyword+'%\''
    print(sql)
    inf = SearchDB(sql)
    inf_1 = getstring(inf)
    msg(inf_1)
    return inf_1
#求片長
def find_movie_long(keyword):
    sql = 'SELECT Cname FROM movie WHERE  Cname = \'' + keyword + '\''
    inf = SearchDB(sql)
    inf_1 = getstring(inf)
    msg(inf_1)
    return inf_1
#求電影排行
def find_movie_recommend():
    sql = 'SELECT Cname FROM movie WHERE Evaluation!="尚無資料" ORDER BY Evaluation DESC LIMIT 5'
    inf = SearchDB(sql)
    inf_1 = getstring(inf)
    msg(inf_1)
    return inf_1
#求類型電影排行
def find_movie_mix_recommend(keyword):
    sql = 'SELECT Cname FROM movie,movie_type WHERE Evaluation!="尚無資料" AND Type = '+'\"'+ keyword +'\"'+ ' AND Tnum=MNum ORDER BY Evaluation DESC LIMIT 5'
    inf = SearchDB(sql)
    inf_1 = getstring(inf)
    msg(inf_1)
    return inf_1
#找詳細資訊
def find_data(inf):
    name = []
    for i in inf:
        i = str(i)
        i=i.strip('(')
        i=i.strip(')')
        i=i.strip('\'')
        i=i.strip(',')
        i = i.strip('\'')
        name.append(i)
    SQL = 'SELECT * FROM movie WHERE Cname = '+'\''+ name[0] +'\''
    for i in name[1:]:
        print(i)
        SQL = SQL +' OR Cname ='+'\''+ i +'\''
        print(SQL)
    print(SQL)
    # cursor.execute(SQL)
    # INF = cursor.fetchall()
    SQL_2 = 'SELECT Tnum,Type FROM movie,movie_type WHERE Tnum = Mnum AND Cname = ' + '\'' + name[0] + '\''
    for i in name[1:]:
        # print(i)
        SQL_2 = SQL_2 +' OR Cname ='+'\''+ i +'\''
        # print(SQL_2)
    # print(SQL_2)
    SQL_3 = 'SELECT Anum,Actor FROM movie,movie_actor WHERE Anum = Mnum AND Cname = ' + '\'' + name[0] + '\''
    for i in name[1:]:
        # print(i)
        SQL_3 = SQL_3 +' OR Cname ='+'\''+ i +'\''
        # print(SQL_3)
    # print(SQL_3)
    SQL_4 = 'SELECT Dnum,Director FROM movie,movie_director WHERE Dnum = Mnum AND Cname = ' + '\'' + name[0] + '\''
    for i in name[1:]:
        # print(i)
        SQL_4 = SQL_4 + ' OR Cname =' + '\'' + i + '\''
        # print(SQL_4)
    # print(SQL_4)
    return

# keyword = "廖慧珍"
# inf = find_movie_actor(keyword)
# print(inf)
#str = 'CNmae LIKE \'% ??%\'' #CNmae LIKE '% ??%  '
#print(str)

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)


@app.route("/")
def verify():
    print('hello')
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(req)
    start=None
    end=None
    keyword=None
    if 'any' in req['queryResult']['parameters']:
        if req.get("queryResult").get("action") == 'ask_movie':
            keyword = req['queryResult']['parameters']['any']
            res = {"fulfillmentText": find_movie_information(keyword)}
        elif req.get("queryResult").get("action") == 'ask_actor':
            keyword = req['queryResult']['parameters']['any']
            res = {"fulfillmentText": find_movie_actor(keyword)}
            #find_movie_actor(keyword)
        elif req.get("queryResult").get("action") == 'ask_category':
            keyword = req['queryResult']['parameters']['any']
            res = {"fulfillmentText": find_movie_category(keyword)}
            #find_movie_category(keyword)
        elif req.get("queryResult").get("action") == 'ask_introduce':
            keyword = req['queryResult']['parameters']['any']
            res = {"fulfillmentText": find_movie(keyword)}
            #find_movie(keyword)
        elif req.get("queryResult").get("action") == 'ask_long':
            keyword = req['queryResult']['parameters']['any']
            res = {"fulfillmentText": find_movie_long(keyword)}
            #find_movie_long(keyword)
        elif req.get("queryResult").get("action") == 'ask_recommend':
            res = {"fulfillmentText": find_movie_recommend()}
            # find_movie_long(keyword)
        elif req.get("queryResult").get("action") == 'ask_mix_recommend':
            keyword = req['queryResult']['parameters']['any']
            res = {"fulfillmentText": find_movie_mix_recommend(keyword)}
            # find_movie_long(keyword)
    elif 'date' in req['queryResult']['parameters']:
        if req['queryResult']['parameters']['date'] != '':
            date = parser.parse(req['queryResult']['parameters']['date'])
            start = date.date()
            res = {"fulfillmentText": find_movie_date(start, end)}
            find_movie_date(start, end)
        elif req['queryResult']['parameters']['date-period'] != '':
            start = parser.parse(req['queryResult']['parameters']['date-period']['startDate']).date()
            end = parser.parse(req['queryResult']['parameters']['date-period']['endDate']).date()
            res = {"fulfillmentText": find_movie_date(start, end)}
            find_movie_date(start, end)
    else:
        if req.get("queryResult").get("action") == 'ask_recommend':
            res = {"fulfillmentText": find_movie_recommend()}
            # find_movie_long(keyword)

    return make_response(jsonify(res))

if __name__ == '__main__':
    app.run(port=5000)