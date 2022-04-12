from flask import Flask, render_template
from db import *
from patientsearchform import PatientSearchForm
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    # status = insert_emp('client', 'John', 'D', 'Doe', 12, 'Toronto', 'Ontario', 123123123, 'JohnDoe@gmail.com', 'male')
    # if ("ERROR" in status):
    #     return status
    num = 12
    return f"Hello World! page has rendered!<h1>{num}<h1>"

@app.route("/users")
def user_info():
    print(get_users())
    return "Users page has rendered!"

@app.route("/patient")
def patient():
    form = PatientSearchForm()
    return render_template('patient.html', title ='Patient', form=form)

@app.route("/emp")
def emp_info():
    print(get_emp())
    return "Emp page has rendered!"

if __name__ == "__main__":
    app.run()
