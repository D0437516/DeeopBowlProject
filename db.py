import pymysql
import json
from flask import json
def openDB():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        port= 3306,
        password='0604',
        database='project',
        charset='utf8'
    )
    return db

def test():
    conn = openDB()
    cursor = conn.cursor()
    inf = 'SELECT * FROM movie WHERE MNum<10'
    cursor.execute(inf)
    INF = cursor.fetchall()

    t = 'SELECT Tnum,Type FROM movie, movie_type WHERE Tnum = MNum AND MNum<10'
    cursor.execute(t)
    TYPE = cursor.fetchall()

    a = 'SELECT Anum,Actor FROM movie, movie_actor WHERE Anum = MNum AND MNum<10'
    cursor.execute(a)
    ACTOR = cursor.fetchall()

    d = 'SELECT Dnum,Director FROM movie, movie_director WHERE Dnum = MNum AND MNum<10'
    cursor.execute(d)
    DIRECTOR= cursor.fetchall()
    content = ''

    data = to_list(INF, TYPE, ACTOR, DIRECTOR)
    return  data

def to_list(INF, TYPE, ACTOR, DIRECTOR):
    Cname = []
    Ename = []
    Date = []
    Time = []
    Type = []
    Actor = []
    Director = []
    Company = []
    IMDb = []
    Eval = []
    Content = []
    Video = []
    Picture = []
    for i in INF:
        Cname.append(i[1])
        Ename.append(i[2])
        Date.append(str(i[3]))
        Time.append(i[4])
        Company.append(i[5])
        IMDb.append(i[6])
        Eval.append(i[7])
        Content.append(i[8])
        Video.append(i[9])
        Picture.append(i[10])

    Type = grouping(TYPE)
    Actor = grouping(ACTOR)
    Director = grouping(DIRECTOR)
    DATA = []
    temp = {}
    for i in range(len(INF)):

        temp['Cname'] = Cname[i]
        temp['Ename'] = Ename[i]
        temp['Date'] = Date[i]
        temp['Time'] = Time[i]
        temp['Type'] = Type[i]
        temp['Actor'] = Actor[i]
        temp['Director'] = Director[i]
        temp['Company'] = Company[i]
        temp['IMDb'] = IMDb[i]
        temp['Eval'] = Eval[i]
        temp['Content'] = Content[i]
        temp['Video'] = Video[i]
        temp['Picture'] = Picture[i]
        DATA.append(temp)

        temp = {}

    #Json_Data = json.dumps(DATA, ensure_ascii=False, sort_keys=True, indent=4)
     #print(type(Json_Data))
    return  DATA
    #
    #
    #     data = {
    #         'Cname': Cname[i], 'Ename': Ename[i], 'Date':Date[i], 'Time':Time[i],
    #         'Type': Type[i],'Actor': Actor[i], 'Director': Director[i], 'Company' : Company[i],
    #         'IMDb' : IMDb[i], 'Eval': Eval[i], 'Content' : Content[i], 'Video': Video[i], 'Picture': Picture[i]
    #      }
    #     STEP_1 = json.dumps(data, ensure_ascii=False)
    #     STEP_2.append(STEP_1)
    #
    # return STEP_2
def grouping(A):
    B = []
    string = ''
    temp = -1
    for i in A:
        if len(i) == 2:
            if i[0] != temp and temp != -1:
                B.append(string)
                string = ''
            string += ' '+ i[1]
            if string != '' and i == A[len(A) - 1]:
                B.append(string)
        else:
            B.append(i[1])
        temp = i[0]
    return B





