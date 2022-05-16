from pickle import NONE
from flask import Flask, redirect, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)

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
    query = f"SELECT * FROM Student WHERE email='{email}';"
    conn.row_factory = sqlite3.Row
    cur.execute(query)
    data = cur.fetchall()
    if(data):
        return True
    else:
        return False

def add_account(fname, mname, lname, dob, phone, gender, home, email, pwd, program):
    try:
        conn = sqlite3.connect('UniversityPortal.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Student (Program_ID, First_Name, Middle_Name, Last_Name, Date_Of_Birth, Home_Address, Email, Password, Phone, Gender) \
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (program, fname, mname, lname, dob, home, email, pwd, phone, gender))
        conn.commit()
    except:
        print("Error!")


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
#add_account("Paul", "Ramisan", "Nievas", "2022-5-4", "669-274-6179", "Male", "123, 9543, CA", "abc@gmail.com", "asd", 1)

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
        query = f"SELECT * FROM Student WHERE Email='{email}' AND Password='{password}';"
        conn.row_factory = sqlite3.Row
        cur.execute(query)
        info = cur.fetchone()

        if(info):
                print((info))
                return render_template("dashboard.html", info=info)
        else:
                error = "Invalid credentials!"
                return render_template("login.html", error=error)

       
@app.route('/applynow/', defaults={'msg':None, 'error':None})       
@app.route('/applynow/<msg>/<error>')
def applynow(msg, error):
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Program")
    programs = cur.fetchall()
    return render_template("register.html",programs=programs, msg=msg, error=error)

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    msg=None
    if request.method == 'POST':

        #Name
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        #DOB-Phone-Gender
        dob = request.form['dob']
        phone = request.form['phone']
        gender = request.form['gender']
        #Home Address
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        country = request.form['country']
        home = street +", "+ city +", "+state+" "+zip+", "+country
        #Email-Password
        email = request.form['email']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']
        #Program
        program = request.form['program']

        if(not check_duplicate(email)):
            if pwd != cpwd:
                msg = "Password do not matched! Please try again."
                return redirect(url_for("applynow", msg=msg, error='True'))
            else:
                add_account(fname, mname, lname, dob, phone, gender, home, email, pwd, program)
                msg = "Account has been registered successfully!"
                return redirect(url_for("applynow", msg=msg, error='False'))
        else:
            msg = "Account already exist!"
            return redirect(url_for("applynow", msg=msg, error='True'))
            

if __name__ == '__main__':
    app.run(debug=True)