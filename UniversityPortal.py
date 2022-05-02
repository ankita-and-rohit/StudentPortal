from pickle import NONE
from flask import Flask, redirect, render_template, request, url_for
import sqlite3
app = Flask('__name__')

conn = sqlite3.connect('UniversityPortal.db')
cur = conn.cursor()


def db_con():
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
    
def init():
    cur.execute("""CREATE TABLE IF NOT EXISTS accounts (
            id integer primary key,
            email text,
            pass text);""")

def check_duplicate(email):
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
    query = f"SELECT * FROM accounts WHERE email='{email}';"
    conn.row_factory = sqlite3.Row
    cur.execute(query)
    data = cur.fetchall()
    if(data):
        return True
    else:
        return False

def add_account(email, password):
    try:
        conn = sqlite3.connect('UniversityPortal.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO accounts (email, pass) VALUES (?, ?)",
                        (email, password))
        conn.commit()
    except:
        pass


def delete_user(id):
    try:
        db_con()
        cur.execute("DELETE FROM accounts WHERE id = " + str(id))
        conn.commit()
    except:
        pass


def fetchAllUsers():
    db_con()
    conn.row_factory = sqlite3.Row
    cur.execute("SELECT * FROM users")
    datas = cur.fetchall()
    return datas
    
#init()
#add_account("paulaldrichnievas@gmail.com", "pass123")
#delete_user(1)

@app.route('/')
def index():
        return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pwd']

        conn = sqlite3.connect('UniversityPortal.db')
        cur = conn.cursor()
        query = f"SELECT * FROM accounts WHERE email='{email}' AND pass='{password}';"
        conn.row_factory = sqlite3.Row
        cur.execute(query)
        data = cur.fetchall()

        if(data):
                return render_template("dashboard.html", email=email)
        else:
                error = "Invalid credentials!"
                return render_template("login.html", error=error)
        
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register', methods=['GET', 'POST'])
def registerACC():
    msg=None
    if request.method == 'POST':
        email = request.form['email']
        pass1 = request.form['pwd1']
        pass2 = request.form['pwd2']

        if(not check_duplicate(email)):
            if pass1 != pass2:
                msg = "Password do not matched! Please try again."
                return render_template("register.html", msg=msg, error=True)
            else:
                add_account(email, pass1)
                msg = "Account has been registered successfully!"
                return render_template("register.html", msg=msg, error=False)
        else:
            msg = "Account already exist!"
            return render_template("register.html", msg=msg, error=True)
            

if __name__ == '__main__':
    app.run(debug=True)