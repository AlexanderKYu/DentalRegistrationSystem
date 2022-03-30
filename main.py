from flask import Flask
from db import *
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('sys.db')
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/")
def home():
    status = insert_users('client', 'John', 'D', 'Doe', 12, 'Toronto', 'Ontario', 123123123, 'JohnDoe@gmail.com', 'male')
    if ("ERROR" in status):
        return status
    return "Hello World! page has rendered!"

@app.route("/users")
def user_info():
    print(get_users())
    return "Users page has rendered!"


# SQL functions

def insert_users(role, first_name, middle_initial, last_name, street_number, city, province, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE SSN = {SSN}")
    list = c.fetchall()
    if(SSN >  999999999):
        return "ERROR: Invalid SSN"
    elif (len(list) != 0):
        return "ERROR: SSN is already in the system"

    c.execute(f"""INSERT INTO users (role, first_name, middle_initial, last_name, street_number, city, province, SSN, email, gender)
                  VALUES ('{role}', '{first_name}', '{middle_initial}', '{last_name}', {street_number}, '{city}', '{province}', {SSN}, '{email}', '{gender}');""")
    conn.commit()
    return "S"

def get_users():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users")
    conn.commit()
    return c.fetchall()

def get_users_ID(ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE ID = {ID}")
    conn.commit()
    return c.fetchone()

if __name__ == "__main__":
    app.run()
    # insert_users('emp', 'Alexis', 'R', 'Verana', 42, 'Ottawa', 'Ontario', 987654321, 'avera085@uottawa.ca', 'female')
