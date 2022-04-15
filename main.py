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
       
       try:
            if "app" in request.form:
                patientApp = get_appointment_list_patient_info(patientID)

                nums = ''
                for x in patientApp:
                    for y in x:
                        print(y)
                        nums += str(y) + '&'
                        
                nums = nums[:-1]
                return redirect(url_for('patient_app', patientApp = nums))
            
            elif "treatment" in request.form: 
                return redirect(url_for('patient_treatment', patientID = patientID))
        
            elif "invoice" in request.form: 
                return redirect(url_for('patient_invoice', patientID = patientID))

       except IndexError:
            #return ("No previous or upcoming appointments to show. Have a good!")
            return "error bruv"

    return render_template('patient.html', title='Patient', form=form)

@app.route("/patient_app", methods=['GET', 'POST'])
def patient_app():

    form = PatientAppForm()
    patientAppId = request.args.get('patientApp')
    nums = patientAppId.split('&')

    table = []
    for x in nums:
        app = []
        data = get_appointment_appointment_ID(x)
        app.append(data[3])
        app.append(data[4])
        app.append(data[5])
        app.append(data[6])
        app.append(data[7])
        app.append(data[8])
        table.append(app)
    
    print("Table " + str (table))
    return render_template('patient_app.html', table=table)  

@app.route("/patient_treatment", methods=['GET', 'POST'])
def patient_treatment():
    patientId = request.args.get('patientID')
    matrixEntry = get_record_patient_ID(patientId)

    treatment = []

    for x in matrixEntry:
        treatment.append(x[1])

    table = []
    for y in treatment:
        row = []
        data = get_treatment_treatment_ID(y)
        # appointment type index = 1
        appID = get_appointment_appointment_ID(data[1])
        row.append(appID[6])
        row.append(data[3])
        row.append(data[4])
        symp = get_symptom_treatment_ID(y)[0]
        row.append(symp[1])
        appPro = get_appointment_procedure_appointment_ID(y)[0]
        row.append(appPro[6])
        row.append(data[5])
        table.append(row)

    return render_template('patient_treatment.html', table=table)

@app.route("/patient_invoice", methods=['GET', 'POST'])
def patient_invoice():
    
    patientId = request.args.get('patientID')
    matrixEntry = get_invoice_patient_ID(patientId)
    users = get_users_ID(patientId)
    table2 = []
    fName = users[2]
    table2.append(fName)
    mInit = users[3]
    if (users[3] == None):
        mInit= ''
    table2.append(mInit)
    lName = users[4]
    table2.append(lName)
    street_number = users[5]
    table2.append(street_number)
    street_name = users[6]
    table2.append(street_name)
    apt = users[7]
    if (users[7] == None):
        apt= ''
    table2.append(apt)
    city = users[8]
    table2.append(city)
    province = users[9]
    table2.append(province)
    code = users[10]
    table2.append(code)
    email = users[12]
    table2.append(email)
    insurance = get_pat_ID(patientId)[1]
    table2.append(insurance)
    phone = get_phone_ID(patientId)
    phoneString = ''
    for a in phone:
        phoneString += a[1] + ': ' + a[2] + ' '
    table2.append(phoneString)

    table = []
    for x in matrixEntry:
        row = []
        row.append(x[1])
        row.append(x[3])
        row.append(x[4])
        row.append(int(x[3]) + int(x[4]))
        row.append(x[5])
        row.append(x[6])
        table.append(row)

    return render_template('patient_invoice.html', table=table, table2=table2)  

@app.route("/emp")
def emp_info():
    print(get_emp())
    return "Emp page has rendered!"

if __name__ == "__main__":
    app.run()
