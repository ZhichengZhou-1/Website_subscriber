from flask import Flask, render_template, request
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector



app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="zzc521",
    database="testdb"
)
mycursor = mydb.cursor()

subscribers = []

@app.route('/')
def index():
    title = "Z's testing site"
    return render_template("index.html", title=title)


@app.route('/about')
def about():
    title = "About Z here!"
    names = ["john", "merry", "wes", "kelly"]
    return render_template("about.html", names = names, title = title)


@app.route('/subscribe')
def subscribe():
    title = "Subscribe to my email"
    return render_template("subscribe.html", title=title)


@app.route('/form', methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    message = first_name + last_name + email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("lhaha9443@gmail.com", "zzc5211314")
    server.sendmail("lhaha9443@gmail.com", email, message)
    server.quit()
    subscribers.append(f"{first_name} {last_name} | {email}")
    mycursor.execute("CREATE TABLE testdb (first_name TEXT, last_name TEXT, email VARCHAR(50), PRIMARY KEY(email))")
    sql = "INSERT INTO testdb (first_name, last_name, email) VALUES (%s, %s, %s)"
    val = (first_name, last_name, email)
    mycursor.execute(sql, val)
    mydb.commit()
    title = "form processing"
    return render_template("form.html", subscribers = subscribers)


if __name__ == "__main__":
    app.run(host = "localhost", port = 3001, debug = True)

