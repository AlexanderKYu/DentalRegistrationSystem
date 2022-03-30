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

    c.execute("""CREATE TABLE IF NOT EXISTS employee (
                 ID INTEGER UNIQUE NOT NULL,
                 employee_type VARCHAR(20) NOT NULL,
                 salary INTEGER NOT NULL,
                 FOREIGN KEY (ID) REFERENCES users(ID)
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

    # c.execute("""CREATE TABLE IF NOT EXISTS branch (
    #              branch_ID INTEGER NOT NULL,
    #              street_number INTEGER NOT NULL,
    #              street_name VARCHAR(20) NOT NULL,
    #              city VARCHAR(20) NOT NULL,
    #              province VARCHAR(20) NOT NULL,
    #              postal_code VARCHAR(20) NOT NULL,
    #              manager INTEGER NOT NULL,
    #              num_of_receptionist INTEGER NOT NULL,
    #              PRIMARY KEY (branch_ID),
    #              FOREIGN KEY (manager) REFERENCES employee(ID)
    #              );
    # """)
    conn.commit()

# Only use this function after the termination of all data / tables
# def initialize_data():
#     conn = db_connection()
#     c = conn.cursor()
#     db_init()
#     c.execute(f"INSERT INTO users VALUES (1, 'admin_role', 'f_name', 'm_init', 'l_name', 1, 'street', NULL, 'city', 'province', 'A1AB2B', 999999999, 'admin@email.com', 'gender')")
#     conn.commit()

# Do not use this function unless needed
# def delete_all_data():
#     conn = db_connection()
#     c = conn.cursor()
#     c.execute(f"DROP TABLE IF EXISTS users")
#     c.execute(f"DROP TABLE IF EXISTS employee")
#     c.execute(f"DROP TABLE IF EXISTS patient")
#     db_init()
#     conn.commit()

# Make sure the data is initialized by the function initialize_data
def create_sample_data():
    insert_emp(60000, 'emp', 'Alexander', 'KS', 'Yu', 27, 'Ambercroft', 'NULL', 'Scarborough', 'ON', 'M1W2Z6', 300120635, 'ayu041@uottawa.ca', 'male')
    insert_emp(65000, 'den', 'Alexis', 'R', 'Verana', 90, 'University', 'NULL', 'Ottawa', 'ON', 'K1N6N5', 300116080, 'avera086@uottawa.ca', 'female')
    insert_emp(60000, 'recep', 'Vanisha', 'NULL', 'Bagga', 45, 'Mann', 36, 'Ottawa', 'ON', 'K1N6Y7', 300191679, 'vbagg019@uottawa.ca', 'female')
    insert_emp(62000, 'dass', 'Christiane', 'A', 'Meherete', 350, 'Victoria', 'NULL', 'Toronto', 'ON', 'M5B2K3', 300116269, 'cmehe017@uottawa.ca', 'female')
    insert_emp(65000, 'den', 'Coralie', 'B', 'Ostertag', 27, 'College', 'NULL', 'Toronto', 'ON', 'M5S1A1', 300174530, 'coste017@uottawa.ca', 'female')

    # insurance, date_of_birth, age, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender
    insert_pat('Manulife', '1972/12/15', 49, 'pat', 'Emily', 'R', 'Cruz', 23, 'King Edward', 'NULL', 'Ottawa', 'ON', 'K2N5G6', 151312658, 'emil54@yahoo.ca', 'female')
    insert_pat('Desjardins', '1999/06/25', 21, 'pat', 'Sheena', 'M', 'Lam', 4, 'Rideau', 'NULL', 'Ottawa', 'ON', 'K1N2F3', 192568463, 'sheeshna09@gmail.com', 'female')

# Please do not use this function to insert, use the insert_emp or insert_pat
def insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE SSN = {SSN}")
    list = c.fetchall()
    if(SSN >  999999999):
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

def insert_emp(salary, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    entry = insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender)
    conn.commit()
    if (isinstance(entry, str)):
        return entry
    c.execute(f"""INSERT INTO employee (ID, employee_type, salary)
                  VALUES ({entry[0]}, '{role}', {salary});""")
    conn.commit()
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

def main():
    return 0
    # delete_all_data()
    # initialize_data()
    # create_sample_data()
    # print(get_users())
    # print("---")
    # print(get_emp())
    # print("---")
    # print(get_pat())

main()
