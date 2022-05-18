from pickle import NONE
from flask import Flask, redirect, render_template, request, url_for, session
import sqlite3
app = Flask('__name__')

conn = sqlite3.connect('UniversityPortal.db')
cur = conn.cursor()

userEmail = str()

app.secret_key = b'478pajj&YOIJdhfjhd'


def db_con():
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
    
def init():
    conn = sqlite3.connect('UniversityPortal.db')
    cur = conn.cursor()
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

@app.route('/')
def index():
        return render_template("login.html")

userEmail = ""
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        email = request.form['email']
        userEmail = email
        password = request.form['pwd']

        conn = sqlite3.connect('UniversityPortal.db')
        cur = conn.cursor()
        query = f"SELECT * FROM accounts WHERE email='{email}' AND pass='{password}';"
        conn.row_factory = sqlite3.Row
        cur.execute(query)
        data = cur.fetchall()

        if(data):
            session.clear()
            session["user_email"] = email
            allCourses = [c[1] for c in getAllCourses()]
            coursesForStudent = [c[1] for c in getAllCoursesForStudent(email)]
            coursesStudentNotIn = subtractLists(allCourses, coursesForStudent)
            return render_template("dashboard.html", email=email, courses = coursesForStudent, coursesAvailable = coursesStudentNotIn)
        else:
                error = "Invalid credentials!"
                return render_template("login.html", error=error)

@app.route('/dashboard')
def addCourse():
    return render_templates("addCourse.html")
            
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/addCourse', methods=['GET', 'POST'])
def addCourseSubmit():
    email = session.get("user_email")

    allCourses = [c[1] for c in getAllCourses()]
    
    if request.method == 'POST':
        course = request.form['course']
        addCourseForStudent(email, course)
        coursesForStudent = [c[1] for c in getAllCoursesForStudent(email)]
        coursesStudentNotIn = subtractLists(allCourses, coursesForStudent)
        return render_template("dashboard.html", email=email, courses = coursesForStudent, coursesAvailable = coursesStudentNotIn)

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

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))
            

if __name__ == '__main__':
    app.run(debug=True)
