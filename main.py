import traceback
import pymysql
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

def openDB():
     db = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='0604',
            database='project',
            charset='utf8'
        )
     return db

def get():
    account = request.args.get('user')
    password = request.args.get('password')
    return account,password

@app.route('/user_register/', methods=["GET"])
def registuser():
    (account, password) = get()
    sql = 'INSERT INTO member VALUES ( \'' + account + '\',\'' + password +'\')'
    conn = openDB()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        return 'SUCESS '
    except:
        traceback.print_exc()
        conn.rollback()
        return 'ERROR !!! CANNOT REGISTER.'
    conn.close()

@app.route('/user_login/', methods=["GET"])
def login():
    (account, password) = get()
    sql = 'SELECT * FROM member WHERE username = \''+account+'\' AND userpass =\''+password+'\''
    conn = openDB()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(len(result))
        if len(result) == 1:
            return 'LOGIN SUCESS'
        else:
            return 'NOT CORRECT'
        conn.connit()
    except:
        traceback.print_exc()
        conn.rollback()
        conn.close()




if __name__ == '__main__':
    app.run(debug=True)
