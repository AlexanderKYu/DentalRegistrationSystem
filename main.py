from flask import Flask, render_template, flash, request
from db import *
from patientsearchform import PatientSearchForm
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = '6f80377f374a443dd2288eb00e322026'



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

@app.route("/patient", methods=['GET', 'POST'])
def patient():
    form = PatientSearchForm()

    if request.method == "POST":
       first_name = request.form.get("fname")

       last_name = request.form.get("lname") 

       dob = request.form.get("dob")

       patientID = get_pat_fName_LName_DOB(first_name, last_name, dob)[0][0]
       
       return "record " + str (get_record_patient_ID(patientID))


    return render_template('patient.html', title ='Patient', form=form)

@app.route("/emp")
def emp_info():
    print(get_emp())
    return "Emp page has rendered!"

if __name__ == "__main__":
    app.run()
