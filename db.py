import sqlite3

conn = sqlite3.connect('sys.db')
c = conn.cursor()

def initialize_table():
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                role VARCHAR(20) NOT NULL,
                first_name VARCHAR(20) NOT NULL,
                middle_initial VARCHAR(20) NOT NULL,
                last_name VARCHAR(20) NOT NULL,
                street_number INTEGER NOT NULL,
                city VARCHAR(20) NOT NULL,
                province VARCHAR(20) NOT NULL,
                SSN INTEGER NOT NULL,
                email VARCHAR(40) NOT NULL,
                gender VARCHAR(20) NOT NULL,
                CONSTRAINT valid_SSN CHECK (SSN <= 999999999)
                );
    """)

def db_init():
    initialize_table()

db_init()
