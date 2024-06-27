import joblib
from peewee import *
from flask import Flask, render_template, request, redirect, session

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__, static_url_path='/static')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/codingthunder'
db = SQLAlchemy(app)


app.secret_key = "jgfsdhjg"
class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

db = SqliteDatabase("database.db")

class User(Model):
    class Meta:
        database = db
    username = CharField()
    password = CharField()
    email = CharField()
  

db.create_tables([User])
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/predict")
def form():
   return render_template('form.html')

@app.route('/form', methods=["POST"])
def brain():
    Nitrogen=float(request.form['Nitrogen'])
    Phosphorus=float(request.form['Phosphorus'])
    Potassium=float(request.form['Potassium'])
    Temperature=float(request.form['Temperature'])
    Humidity=float(request.form['Humidity'])
    Ph=float(request.form['ph'])
    Rainfall=float(request.form['Rainfall'])
     
    values=[Nitrogen,Phosphorus,Potassium,Temperature,Humidity,Ph,Rainfall]
    
    if Ph>0 and Ph<=14 and Temperature<100 and Humidity>0:
        joblib.load('crop_app','r')
        model = joblib.load(open('crop_app','rb'))
        arr = [values]
        acc = model.predict(arr)
        print(acc, "acc")
        return render_template('prediction.html', prediction=str(acc))
    else:
        return "Sorry...  Error in entered values in the form Please check the values and fill it again"
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')
@app.route("/register.html", methods=["GET", "POST"])
def register():
    message = None
    if request.method == "POST":
        user = User.select().where(User.email==request.form.get("email")).first()
        if not user:
            User.create(
                username = request.form.get("username"),
                 email = request.form.get("email"),
                password= request.form.get("password")
         
               
            )
            message = "You are registerd"
        else:
            message = "Please chek your details"

    return render_template("register.html", msg=message)

@app.route("/login.html", methods=["POST", "GET"])
def login():
    msg = None
    if request.method == "POST":
        u = request.form.get("email")
        p = request.form.get("password")
        if User.select().where(
            User.email == u
        ).where(
            User.password ==p
        ):
            session["login"] = True
            return redirect("/index.html")
        
        msg = "You are loggined"
    # else:
        # msg = "Invalid username or password"
    return render_template("login.html", msg=msg)


app.run(debug=True)


