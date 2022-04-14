from flask import Flask, render_template, flash, request, redirect, url_for
from db import *
from patientsearchform import PatientSearchForm
from patientChooseForm import PatientChooseForm
from patientAppForm import PatientAppForm
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
       
       print("PATIENT  " + str(patientID))
 
       try:
            return str (get_appointment_list_patient_info(patientID)[0]) ##past appointment and future appointment

       except IndexError:
            #return ("No previous or upcoming appointments to show. Have a good!")

            if "app" in request.form:
                print("APPOINTMENT OPEN")
                print("APPOINTMENT ID  " + str(patientID))
        
                return redirect(url_for('patient_app', patientID = patientID))
    
            elif "treatment" in request.form: 
                print("TREATMENT OPEN")

                return redirect(url_for('patient_treatment', patientID = patientID))
        
            elif "invoice" in request.form: 
                print("INVOICE OPENs")

                return redirect(url_for('patient_invoice', patientID = patientID))
            
            #return redirect(url_for('patient_2', patientID = patientID))  #OPENS NEXT PAGE

    
    return render_template('patient.html', title='Patient', form=form)
    #return render_template('patientChoose.html', title='PatientChoose')

# @app.route("/patient_2", methods=['GET', 'POST'])
# def patient_2():
#     form = PatientChooseForm()

#     patientID = request.args.get('patientID')
#     #return "PATIENT CHOOSE " + str(patientID) 

#     print("PATIENT CHOOSE  " + str(patientID))
#     print("STILL  " +  str(patientID))

#     if "app" in request.form:
#         print("APPOINTMENT OPEN")
#         print("APPOINTMENT ID  " + str(patientID))
#         return redirect(url_for('patient_app', patientID = patientID))
    
#     elif "treatment" in request.form: 
#         print("TREATMENT OPEN")
#         return redirect(url_for('patient_treatment', patientID = patientID))
    
#     elif "invoice" in request.form: 
#         print("INVOICE OPENs")
#         return redirect(url_for('patient_invoice', patientID = patientID))

#     return render_template('patient_2.html')  


@app.route("/patient_app", methods=['GET', 'POST'])
def patient_app():

    form = PatientAppForm()

    patientID = request.args.get('patientID')
    #return "PATIENT CHOOSE " + str(patientID) 

    print("PATIENT APP  " + str(patientID))
    print("STILL APP  " +  str(patientID))

    return render_template('patient_app.html')  



@app.route("/patient_treatment", methods=['GET', 'POST'])
def patient_treatment():

    return render_template('patient_treatment.html')  

@app.route("/patient_invoice", methods=['GET', 'POST'])
def patient_invoice():

    return render_template('patient_invoice.html')  




@app.route("/emp")
def emp_info():
    print(get_emp())
    return "Emp page has rendered!"

if __name__ == "__main__":
    app.run()
