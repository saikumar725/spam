from flask import Flask,render_template,redirect,session,url_for,request
from flask_mysqldb import MySQL
import MySQLdb
app = Flask(__name__)
app.secret_key='saikumar'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = " Admin@1234"
app.config["MYSQL_DB"] = "login"


@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM logininfo WHERE username=%s AND password=%s",(username,password))
            info = cursor.fetchone()
            if info['username'] == username and info['password'] == password:
                return "login successfull"
            else:
                return "login unsuccessful,please register"
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)

