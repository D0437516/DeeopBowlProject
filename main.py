import traceback
import pymysql
from flask import Flask
from flask import render_template
from flask import request
import json
import  db
from flask import Response
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')



def get():
    account = request.args.get('user')
    password = request.args.get('password')
    return account,password

@app.route('/user_register/', methods=["GET"])
def registuser():
    (account, password) = get()
    sql = 'INSERT INTO member VALUES ( \'' + account + '\',\'' + password +'\')'
    conn = db.openDB()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        return render_template('index_success.html',name=account)
    except:
        traceback.print_exc()
        conn.rollback()
        return 'ERROR !!! CANNOT REGISTER.'
    conn.close()

@app.route('/user_login/', methods=["GET"])
def login():
    (account, password) = get()
    sql = 'SELECT * FROM member WHERE username = \''+account+'\' AND userpass =\''+password+'\''
    conn = db.openDB()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(len(result))
        if len(result) == 1:

            return render_template('TEST.html',data = db.test())
            #return render_template('index_success.html', name=account)
        else:
            return 'NOT CORRECT'
        conn.connit()
    except:
        traceback.print_exc()
        conn.rollback()
        conn.close()

@app.route('/addListJumpTo/',methods=["GET"]  )
def addlist():
    return render_template('favList.html')



if __name__ == '__main__':

    app.run(debug=True)
