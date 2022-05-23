from pickle import NONE
from flask import Flask, redirect, render_template, request, redirect, url_for, session
import sqlite3
app = Flask(__name__)

conn = sqlite3.connect('UniversityPortal.db')
cur = conn.cursor()

userEmail = str()
app.secret_key = b'478pajj&YOIJdhfjhd'

def db_con():
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
    
def init():
    print('init method.')
    cur.execute("""CREATE TABLE IF NOT EXISTS accounts (
            id integer primary key,
            email text,
            pass text);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS courses (
    id integer primary key,
    name text
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS studentsInCourses (
    id integer primary key,
    email text,
    courseName text,
    unique (email, courseName)
    );""")
    cur.execute("SELECT * FROM courses")
    if not cur.fetchall():
        cur.execute("""INSERT INTO courses (name) VALUES ("Accounting");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("Astronomy");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("Biology");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("Computer Information Systems");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("Calulus");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("Physics");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("Chemistry");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("Economics");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("English Literature");""")
        cur.execute("""INSERT INTO courses (name) VALUES ("Spanish");""")
    conn.commit()


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

def getAllCourses():
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cur.execute("SELECT * FROM courses")
    data = cur.fetchall()
    return data
def getStudentsInCourses():
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cur.execute("SELECT * FROM studentsInCourses")
    data = cur.fetchall()
    return data

def addCourseForStudent(email, courseName) :
  try: 
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
    print("Inserting student ", email, " to course ", courseName)
    cur.execute("INSERT INTO studentsInCourses (email, courseName) VALUES (?, ?)",
                        (email, courseName))
    conn.commit()
  except:
    pass
  
def getAllCoursesForStudent(email) :
  conn = sqlite3.connect('UniversityPortal.db')
  cur = conn.cursor()
  conn.row_factory = sqlite3.Row
  query = f"SELECT email, courseName FROM studentsInCourses INNER JOIN courses ON studentsInCourses.courseName = courses.name WHERE studentsInCourses.email='{email}'"
  cur.execute(query)
  data = cur.fetchall()
  return data

def subtractLists(l1, l2):
    newList = []
    for foo in l1:
        if not foo in l2:
            newList.append(foo)
    return newList
    
init()
#init()
#add_account("paulaldrichnievas@gmail.com", "pass123")
#delete_user(1)
#add_account("Paul", "Ramisan", "Nievas", "2022-5-4", "669-274-6179", "Male", "123, 9543, CA", "abc@gmail.com", "asd", 1)

@app.route('/')
def index():
        return render_template("login.html")

userEmail = ""

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        email = request.form['email']
        userEmail = ""
        password = request.form['pwd']

        conn = sqlite3.connect('UniversityPortal.db')
        cur = conn.cursor()
        query = f"SELECT * FROM Student WHERE Email='{email}' AND Password='{password}';"
        conn.row_factory = sqlite3.Row
        cur.execute(query)
        info = cur.fetchone()

        if(info):
                print((info))
                session.clear()
                session["user_email"] = email
                session["user_info"] = info
                allCourses = [c[1] for c in getAllCourses()]
                coursesForStudent = [c[1] for c in getAllCoursesForStudent(email)]
                coursesStudentNotIn = subtractLists(allCourses, coursesForStudent)
                return render_template("dashboard.html", info=info, courses = coursesForStudent, coursesAvailable = coursesStudentNotIn)
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

@app.route('/addCourse', methods=['GET', 'POST'])
def addCourseSubmit():
    email = session.get("user_email")
    info = session.get("user_info")
    allCourses = [c[1] for c in getAllCourses()]
    
    if request.method == 'POST':
        course = request.form['course']
        addCourseForStudent(email, course)
        coursesForStudent = [c[1] for c in getAllCoursesForStudent(email)]
        coursesStudentNotIn = subtractLists(allCourses, coursesForStudent)
        return render_template("dashboard.html", info=info, courses = coursesForStudent, coursesAvailable = coursesStudentNotIn)

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
            
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)