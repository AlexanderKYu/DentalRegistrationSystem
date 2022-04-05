import sqlite3

# conn = None
# c = None

def db_connection():
    try:
        conn = sqlite3.connect('sys.db')
    except sqlite3.error as e:
        print(e)
    return conn

def db_init():
    conn = db_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                role VARCHAR(20) NOT NULL,
                first_name VARCHAR(20) NOT NULL,
                middle_initial VARCHAR(20),
                last_name VARCHAR(20) NOT NULL,
                street_number INTEGER NOT NULL,
                street_name VARCHAR(20) NOT NULL,
                apt_number INTEGER,
                city VARCHAR(20) NOT NULL,
                province VARCHAR(20) NOT NULL,
                postal_code VARCHAR(6) NOT NULL,
                SSN INTEGER NOT NULL,
                email VARCHAR(40) NOT NULL,
                gender VARCHAR(20) NOT NULL,
                CONSTRAINT valid_SSN CHECK (SSN <= 999999999 AND SSN >= 100000000)
                );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS branch (
                 branch_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 street_number INTEGER NOT NULL,
                 street_name VARCHAR(20) NOT NULL,
                 city VARCHAR(20) NOT NULL,
                 province VARCHAR(20) NOT NULL,
                 postal_code VARCHAR(20) NOT NULL,
                 manager INTEGER,
                 num_of_receptionist INTEGER,
                 FOREIGN KEY (manager) REFERENCES employee(ID)
                 CONSTRAINT valid_recep CHECK (num_of_receptionist <= 2)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS employee (
                 ID INTEGER UNIQUE NOT NULL,
                 employee_type VARCHAR(20) NOT NULL,
                 salary INTEGER NOT NULL,
                 branch_ID INTEGER NOT NULL,
                 FOREIGN KEY (ID) REFERENCES users(ID)
                 FOREIGN KEY (branch_ID) REFERENCES branch (branch_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS patient (
                 ID INTEGER UNIQUE NOT NULL,
                 insurance VARCHAR(20) NOT NULL,
                 date_of_birth VARCHAR(10) NOT NULL,
                 age INTEGER NOT NULL,
                 FOREIGN KEY (ID) REFERENCES users(ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS appointment (
                 appointment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_ID INTEGER NOT NULL,
                 employee_ID INTEGER NOT NULL,
                 date VARCHAR(10) NOT NULL,
                 start_time VARCHAR(5) NOT NULL,
                 end_time VARCHAR(5) NOT NULL,
                 appointment_type VARCHAR(20) NOT NULL,
                 status VARCHAR(20) NOT NULL,
                 room_number INTEGER NOT NULL,
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID),
                 FOREIGN KEY (employee_ID) REFERENCES employee(ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS insurance_claim (
                 claim_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 claim_code INTEGER NOT NULL
                 );
    """)

    # patient_charge and insurance_charge can be null? maybe?
    c.execute("""CREATE TABLE IF NOT EXISTS patient_billing (
                 payment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_ID INTEGER NOT NULL,
                 patient_charge INTEGER NOT NULL,
                 insurance_charge INTEGER NOT NULL,
                 insurance VARCHAR(20) NOT NULL,
                 claim_ID INTEGER NOT NULL,
                 covered_by_emp INTEGER,
                 FOREIGN KEY (claim_ID) REFERENCES insurance_claim(claim_ID),
                 FOREIGN KEY (covered_by_emp) REFERENCES employee(ID),
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID)
                 );
    """)
    # description can be NULL and tooth_involved can also be null if there is no tooth exactly (ex. general cleaning)
    c.execute("""CREATE TABLE IF NOT EXISTS appointment_procedure (
                 appPro_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_ID INTEGER NOT NULL,
                 date VARCHAR(10) NOT NULL,
                 procedure_code INTEGER NOT NULL,
                 procedure_type VARCHAR(20) NOT NULL,
                 description VARCHAR(300),
                 tooth_involved INTEGER,
                 payment_ID INTEGER NOT NULL,
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID),
                 FOREIGN KEY (payment_ID) REFERENCES patient_billing(payment_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS fee_charge (
                 fee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 appPro_ID INTEGER NOT NULL,
                 fee_code INTEGER NOT NULL,
                 charge INTEGER NOT NULL,
                 FOREIGN KEY (appPro_ID) REFERENCES appointment_procedure(appPro_ID)
                 );
    """)
    conn.commit()
    
# -- Create table invoice(
# -- 	appPro_ID integer not null,
# -- 	date_of_issue date not null,
# -- 	patient_ID integer not null,
# -- 	patient_charge integer not null,
# -- 	insurance_charge integer not null,
# -- 	discount integer not null,
# -- 	penalty integer not null,
# -- 	fee_ID integer not null,
# -- 	insurance varchar(20) not null,
# -- 	Foreign Key (appPro_ID) references appointment_procedure(appPro_ID),
# -- 	Foreign Key (patient_ID) references patient(ID),
# -- 	Foreign Key (fee_ID) references fee_charge(fee_ID)
# -- );
#
# -----------------------------------------------------------------------
#
# -- Create table amount(
# -- 	appPro_ID integer not null,
# -- 	quantity integer not null,
# -- 	substance_type varchar(20) not null,
# -- 	Primary Key (amount_ID),
# -- 	Foreign Key (appPro_ID) references appointment_procedure(appPro_ID)
# -- );
#
# -- Create table treatment(
# -- 	treatment_ID integer not null,
# -- 	appointment_ID integer not null,
# -- 	appPro_ID integer not null,
# -- 	appointment_type varchar(20) not null,
# -- 	treatment_type varchar(20) not null,
# -- 	medication varchar(20) not null,
# -- 	tooth_involved integer not null,
# -- 	comment varchar(300),
# -- 	Primary Key (treatment_ID),
# -- 	Foreign Key (appointment_ID) references appointment(appointment_ID),
# -- 	Foreign Key (appPro_ID) references appointment_procedure(appPro_ID)
# -- );
#
# -- Create table Record(
# -- 	patient_ID integer not null,
# -- 	treatment_ID integer not null,
# -- 	Foreign Key (patient_ID) references patient(ID),
# -- 	Foreign Key (treatment_ID) references treatment(treatment_ID)
# -- );
#
# -- Create table Review(
# -- 	patient_ID integer not null,
# -- 	professionalism integer not null,
# -- 	communication integer not null,
# -- 	cleanliness integer not null,
# -- 	value integer not null,
# -- 	Foreign Key (patient_ID) references patient(ID)
# -- );
#
# -- Create table Gurardian(
# -- 	ID integer unique not null,
# -- 	insurance varchar(20) not null,
# -- 	date_of_birth date not null,
# -- 	age integer not null,
# -- 	Foreign Key (ID) references Users(ID)
# -- );
#
# -- Create table phone(
# -- 	ID integer not null,
# -- 	phone_number varchar(16) not null,
# -- 	Foreign Key (ID) references users(ID)
# -- );
#
# -- Create table payment(
# -- 	payment_ID integer not null,
# -- 	payment_type varchar(20) not null,
# -- 	Foreign Key (payment_ID) references patient_billing(payment_ID)
# -- );
#
# -- Create table symptom(
# -- 	treatment_ID integer not null,
# -- 	symptom_type varchar(20) not null,
# -- 	Foreign Key (treatment_ID) references treatment(treatment_ID)
# -- );

# Only use this function after the termination of all data / tables
# def initialize_data():
#     conn = db_connection()
#     c = conn.cursor()
#     db_init()
#     # insert branch first, to insert emp
#     c.execute(f"INSERT INTO branch VALUES (1, 1, 'street_name', 'city', 'province', 'postal_code', 1, 2)")
#     c.execute(f"INSERT INTO users VALUES (1, 'admin_role', 'f_name', 'm_init', 'l_name', 1, 'street', NULL, 'city', 'province', 'A1AB2B', 999999999, 'admin@email.com', 'gender')")
#     conn.commit()

# Do not use this function unless needed
def delete_all_data():
    conn = db_connection()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS employee")
    c.execute("DROP TABLE IF EXISTS patient")
    c.execute("DROP TABLE IF EXISTS branch")
    c.execute("DROP TABLE IF EXISTS appointment")
    c.execute("DROP TABLE IF EXISTS insurance_claim")
    c.execute("DROP TABLE IF EXISTS patient_billing")
    c.execute("DROP TABLE IF EXISTS appointment_procedure")
    c.execute("DROP TABLE IF EXISTS fee_charge")
    db_init()
    conn.commit()

# Make sure the data is initialized by the function initialize_data
def create_sample_data():
    # street_number, street_name, city, province, postal_code, manager, num_of_receptionist
    insert_branch(290, 'Bremner', 'Toronto', 'ON', 'M5V3L9', 'NULL', 0)
    insert_branch(2000, 'Meadowvale', 'Toronto', 'ON', 'M1B5K7', 'NULL', 0)

    # salary, branch_ID, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender
    insert_emp(60000, 2, 'emp', 'Alexander', 'KS', 'Yu', 27, 'Ambercroft', 'NULL', 'Scarborough', 'ON', 'M1W2Z6', 300120635, 'ayu041@uottawa.ca', 'male')
    assign_man(2, 2)
    insert_emp(65000, 3, 'den', 'Alexis', 'R', 'Verana', 90, 'University', 'NULL', 'Ottawa', 'ON', 'K1N6N5', 300116080, 'avera086@uottawa.ca', 'female')
    assign_man(3, 3)
    insert_emp(60000, 2, 'recep', 'Vanisha', 'NULL', 'Bagga', 45, 'Mann', 36, 'Ottawa', 'ON', 'K1N6Y7', 300191679, 'vbagg019@uottawa.ca', 'female')
    insert_emp(62000, 3, 'dass', 'Christiane', 'A', 'Meherete', 350, 'Victoria', 'NULL', 'Toronto', 'ON', 'M5B2K3', 300116269, 'cmehe017@uottawa.ca', 'female')
    insert_emp(65000, 2, 'den', 'Coralie', 'B', 'Ostertag', 27, 'College', 'NULL', 'Toronto', 'ON', 'M5S1A1', 300174530, 'coste017@uottawa.ca', 'female')

    # insurance, date_of_birth, age, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender
    insert_pat('Manulife', '1972/12/15', 49, 'pat', 'Emily', 'R', 'Cruz', 23, 'King Edward', 'NULL', 'Ottawa', 'ON', 'K2N5G6', 151312658, 'emil54@yahoo.ca', 'female')
    insert_pat('Desjardins', '1999/06/25', 21, 'pat', 'Sheena', 'M', 'Lam', 4, 'Rideau', 'NULL', 'Ottawa', 'ON', 'K1N2F3', 192568463, 'sheeshna09@gmail.com', 'female')
    insert_pat('Aviva', '2001/02/13', 21, 'pat', 'Daniel', 'NULL', 'Ng', 5, 'Huntwood', 'NULL', 'Scarborough', 'ON', 'M1W5G7', 753126145, 'dannyphantom@gmail.com', 'male')

    # patient_ID, employee_ID, date, start_time, end_time, appointment_type, status, room_number
    insert_appointment(6, 2, '2022/04/15', '11:25', '13:10', 'cleaning', 'scheduled', 14)

    insert_insurance_claim(5000)
    insert_insurance_claim(6500)

    insert_patient_billing(get_users_SSN(753126145)[0], 250, 50, 'Aviva', 1, 'NULL')

    # patient_ID, date, procedure_code, procedure_type, description, tooth_involved, payment_ID
    insert_appointment_procedure(get_users_SSN(753126145)[0], '2022/04/21', 5, 'cleaning', 'General cleaning', 'NULL', 1)

    # no fee charge as user was not late / cancelled 24 hours before
    # appPro_ID, fee_code, charge
    insert_fee_charge(1, 0, 0)

# Please do not use this function to insert, use the insert_emp or insert_pat
def insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE SSN = {SSN}")
    list = c.fetchall()
    if(SSN >  999999999 or SSN < 99999999):
        print("ERROR: Invalid SSN")
        return "ERROR: Invalid SSN"
    elif (len(list) != 0):
        print("ERROR: SSN is already in the system")
        return "ERROR: SSN is already in the system"

    c.execute(f"""INSERT INTO users (role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender)
                  VALUES ('{role}', '{first_name}', '{middle_initial}', '{last_name}', {street_number}, '{street_name}', {apt_number}, '{city}', '{province}', '{postal_code}', {SSN}, '{email}', '{gender}');""")
    conn.commit()
    entry = get_users_SSN(SSN)
    return entry

def insert_emp(salary, branch_ID, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    entry = insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender)
    conn.commit()
    if (isinstance(entry, str)):
        return entry
    c.execute(f"""INSERT INTO employee (ID, employee_type, salary, branch_ID)
                  VALUES ({entry[0]}, '{role}', {salary}, {branch_ID});""")
    conn.commit()

    if (role == 'recep'):
        status = assign_recep(branch_ID, entry[0])
        if(isinstance(status, str)):
            c.execute(f"""DELETE FROM employee WHERE ID = {entry[0]}""")
            c.execute(f"""DELETE FROM users WHERE ID = {entry[0]}""")
            conn.commit()
            return status
    newEntry = get_emp_ID(entry[0])
    return newEntry

def insert_pat(insurance, date_of_birth, age, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    entry = insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender)
    conn.commit()
    if(isinstance(entry, str)):
        return entry
    c.execute(f"""INSERT INTO patient (ID, insurance, date_of_birth, age)
                  VALUES ({entry[0]}, '{insurance}', '{date_of_birth}', {age})""")
    conn.commit()
    newEntry = get_pat_ID(entry[0])
    return newEntry

def insert_branch(street_number, street_name, city, province, postal_code, manager, num_of_receptionist):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO branch (street_number, street_name, city, province, postal_code, manager, num_of_receptionist)
                  VALUES ({street_number}, '{street_name}', '{city}', '{province}', '{postal_code}', {manager}, '{num_of_receptionist}')""")
    conn.commit()
    entry = get_branch_street(street_number, street_name)
    return entry

def insert_appointment(patient_ID, employee_ID, date, start_time, end_time, appointment_type, status, room_number):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO appointment (patient_ID, employee_ID, date, start_time, end_time, appointment_type, status, room_number)
                  VALUES ({patient_ID}, {employee_ID}, '{date}', '{start_time}', '{end_time}', '{appointment_type}', '{status}', {room_number})""")
    conn.commit()
    entry = get_appointment_patient_info(patient_ID, date)
    return entry

def insert_insurance_claim(claim_code):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO insurance_claim (claim_code)
                  VALUES ({claim_code})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM insurance_claim WHERE rowid = {row_ID}""")
    claim_ID = c.fetchone()[0]
    entry = get_insurance_claim_ID(claim_ID)
    return entry

def insert_patient_billing(patient_ID, patient_charge, insurance_charge, insurance, claim_ID, covered_by_emp):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO patient_billing (patient_ID, patient_charge, insurance_charge, insurance, claim_ID, covered_by_emp)
                  VALUES ({patient_ID}, {patient_charge}, {insurance_charge}, '{insurance}', {claim_ID}, {covered_by_emp})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM patient_billing WHERE rowid = {row_ID}""")
    payment_ID = c.fetchone()[0]
    entry = get_patient_billing_payment_ID(payment_ID)
    return entry

def insert_appointment_procedure(patient_ID, date, procedure_code, procedure_type, description, tooth_involved, payment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO appointment_procedure (patient_ID, date, procedure_code, procedure_type, description, tooth_involved, payment_ID)
                  VALUES ({patient_ID}, '{date}', {procedure_code}, '{procedure_type}', '{description}', {tooth_involved}, {payment_ID})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM appointment_procedure WHERE rowid = {row_ID}""")
    appPro_ID = c.fetchone()[0]
    entry = get_appointment_procedure_appPro_ID(appPro_ID)
    return entry

def insert_fee_charge(appPro_ID, fee_code, charge):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO fee_charge (appPro_ID, fee_code, charge)
                  VALUES ({appPro_ID}, {fee_code}, {charge})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM fee_charge WHERE rowid = {row_ID}""")
    fee_ID = c.fetchone()[0]
    entry = get_fee_charge_fee_ID(fee_ID)
    return entry

def assign_man(branch_ID, manager):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""UPDATE branch SET manager = {manager} WHERE branch_ID = {branch_ID}""")
    conn.commit()

def assign_recep(branch_ID, recep):
    conn = db_connection()
    c = conn.cursor()
    entry = get_branch_branch_ID(branch_ID)
    if (entry[-1] == 2):
        print("ERROR: This branch already has two receptionists")
        return "ERROR: This branch already has two receptionists"
    c.execute(f"""UPDATE branch SET num_of_receptionist = {entry[-1] + 1} WHERE branch_ID = {branch_ID}""")
    conn.commit()

def get_users():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users")
    conn.commit()
    return c.fetchall()

def get_pat():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient")
    conn.commit()
    return c.fetchall()

def get_branch():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM branch")
    conn.commit()
    return c.fetchall()

def get_appointment():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment")
    conn.commit()
    return c.fetchall()

def get_insurance_claim():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM insurance_claim")
    conn.commit()
    return c.fetchall()

def get_patient_billing():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient_billing")
    conn.commit()
    return c.fetchall()

def get_appointment_procedure():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment_procedure")
    conn.commit()
    return c.fetchall()

def get_fee_charge():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM fee_charge")
    conn.commit()
    return c.fetchall()

def get_users_ID(ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE ID = {ID}")
    conn.commit()
    return c.fetchone()

def get_pat_ID(ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient WHERE ID = {ID}")
    conn.commit()
    return c.fetchone()

def get_users_SSN(SSN):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE SSN = {SSN}")
    conn.commit()
    return c.fetchone()

def get_branch_street(street_number, street_name):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM branch WHERE street_number = {street_number} AND street_name = '{street_name}'")
    conn.commit()
    return c.fetchone()

def get_branch_man(manager):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM branch WHERE manager = {manager}")
    conn.commit()
    return c.fetchone()

def get_branch_branch_ID(branch_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM branch WHERE branch_ID = {branch_ID}")
    conn.commit()
    return c.fetchone()

def get_emp():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM employee")
    conn.commit()
    return c.fetchall()

def get_emp_ID(ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM employee WHERE ID = {ID}")
    conn.commit()
    return c.fetchone()

def get_appointment_patient_info(patient_ID, date):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment WHERE patient_ID = {patient_ID} AND date = '{date}'")
    conn.commit()
    return c.fetchone()

def get_insurance_claim_ID(claim_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM insurance_claim WHERE claim_ID = {claim_ID}")
    conn.commit()
    return c.fetchone()

def get_patient_billing_payment_ID(payment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient_billing WHERE payment_ID = {payment_ID}")
    conn.commit()
    return c.fetchone()

def get_appointment_procedure_appPro_ID(appPro_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment_procedure WHERE appPro_ID = {appPro_ID}")
    conn.commit()
    return c.fetchone()

def get_fee_charge_fee_ID(fee_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM fee_charge WHERE fee_ID = {fee_ID}")
    conn.commit()
    return c.fetchone()

def print_tables():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_schema WHERE type='table'")
    print(c.fetchall())

def printer(table, table_name):

    print(f"\nTable: {table_name}\n")
    for x in table:
        print(x)
    print("*******************************************************************")

def main():
    delete_all_data()
    # initialize_data()
    create_sample_data()
    # print_tables()
    printer(get_users(), 'users')
    printer(get_emp(), 'employee')
    printer(get_pat(), 'patient')
    printer(get_branch(), 'branch')
    printer(get_appointment(), 'appointment')
    printer(get_insurance_claim(), 'insurance_claim')
    printer(get_patient_billing(), 'patient_billing')
    printer(get_appointment_procedure(), 'appointment_procedure')
    printer(get_fee_charge(), 'fee_charge')

main()
