from flask import Flask
from db import *
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    # status = insert_emp('client', 'John', 'D', 'Doe', 12, 'Toronto', 'Ontario', 123123123, 'JohnDoe@gmail.com', 'male')
    # if ("ERROR" in status):
    #     return status
    return "Hello World! page has rendered!"

@app.route("/users")
def user_info():
    print(get_users())
    return "Users page has rendered!"

@app.route("/emp")
def emp_info():
    print(get_emp())
    return "Emp page has rendered!"

if __name__ == "__main__":
    app.run()
