
from sqlite3.dbapi2 import Cursor, Date, connect
from flask import Flask, render_template,request,redirect
# from flask.wrappers import Request
# from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import string
import random
import sqlite3
import time

# from randomstringgen import sendrandom
# from actions.actions import sendrandomnumber

# from sqlalchemy.sql import text


# def db_connection():
#     con=None
#     try:
#         con=sqlite3.connect("surveydetails.db")
#     except Exception as e:
#         print(str(e))
#     return con
# db_name = 'surveydetails.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# # # initialize DB
# db=SQLAlchemy(app)

# # create database model

# class SurveyDetails(db.Model):
#     id=db.Column(db.String,primary_key=True)
#     name=db.Column(db.String(200),nullable=False)
#     gender=db.Column(db.String(200),nullable=False)
#     age=db.Column(db.String(200),nullable=False)
#     vaccinestat=db.Column(db.String(200),nullable=False)
#     date_of_survey=db.Column(db.DateTime,default=datetime.utcnow)
#     # create a function to return a string when we add something
#     def __repr__(self) -> str:
#         return super().__repr__()


# @app.route('/profile/<name>')
# def profile(name):
#     return render_template("profile.html",name=name)


# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr} </h1>"




app= Flask(__name__)
# randomstr=''.join(random.choices(string.ascii_letters+string.digits,k=10))
# # print("Random String in the very beginning is : ",randomstr)
# print("Random String in the app is : ",randomstr)
# global randomstr
# global rand
# rand=[]
# randomlist=[]
randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=10))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pre')
def pre():
    # create a randomstring, pass it to post page
    # randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=10))
    return render_template("pre.html")

@app.route('/post')
def post():
    return render_template("post.html")

@app.route('/ca',methods=["POST","GET"])
def ca():
    # global randomstr
    randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=10))
    # randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=10))
    
    if request.method=="POST":
        con=sqlite3.connect("surveydetails.db")
        cursor=con.cursor()
               
        print("Random String got inside function is : ",randomstr)
        person_id=randomstr
        # person_name=request.form['name1']
        person_gender=request.form['agegroup']
        person_age=request.form['gendergroup']
        person_country=request.form['country']
        person_q1=request.form['likert1']
        person_q2=request.form['likert2']
        person_q3=request.form['likert3']
        person_q4=request.form['likert4']
        person_q5=request.form['likert5']
        person_q6=request.form['likert6']
        person_q7=request.form['likert7']
        person_q8=request.form['likert8']
        person_q9=request.form['likert9']
        person_q10=request.form['likert10']
        # chat_start_time=time.time()
        # person_vaccinestat=request.form['vacstatgroup']
        # person_dateofsurvey=int(date('now'))
        try:
            sql="""INSERT INTO SurveyDetails VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            # result=cursor.execute(sql)
            result=cursor.execute(sql,(person_id,person_gender,person_age,person_country,person_q1,person_q2,person_q3,person_q4,person_q5,person_q6,person_q7,person_q8,person_q9,person_q10))
            
            if result==0:
                print("Error in database")
            else:
                print("Success")
            con.commit()
            cursor.close()
            con.close()
            return render_template('ca.html',randomstr=randomstr)
        except Exception as e:
            print(str(e))
            return redirect('/')
    
 

# def sendrandom():
#     print("The randomstring created is : ",randomstr)
#     return randomstr

@app.route('/thankyou',methods=["POST"])
def thankyou():
    
    con=sqlite3.connect("PostSurveyDetails.db")
    cursor=con.cursor()
    person_id=request.form['pcode']
    person_q1=request.form['likert11']
    person_q2=request.form['likert12']
    person_q3=request.form['likert13']
    person_q4=request.form['likert14']
    person_q5=request.form['likert15']
    person_q6=request.form['likert16']
    person_q7=request.form['likert17']
    person_q8=request.form['likert18']
    person_q9=request.form['likert19']
    person_q10=request.form['likert20']
    try:
        sql="""INSERT INTO PostSurveyDetails VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
            # result=cursor.execute(sql)
        result=cursor.execute(sql,(person_id,person_q1,person_q2,person_q3,person_q4,person_q5,person_q6,person_q7,person_q8,person_q9,person_q10))
            
        if result==0:
            print("Error in database")
        else:
            print("Success")
        con.commit()
        cursor.close()
        con.close()
        return render_template('thankyou.html')
    except Exception as e:
        print(str(e))
        return redirect('/')


if __name__=="__main__":
    
    app.run(debug=True)
     