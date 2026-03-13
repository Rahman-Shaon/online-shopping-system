from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "MySQLhello#1",
    database = "flask_shop"
)

cursor = db.cursor()

@app.route("/")
def home():
    return render_template("home.html", name = "Shaon")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/submit", methods = ["POST"])
def submit ():
    username = request.form["username"]

    sql = "INSERT INTO users (username) VALUES (%s)"
    val = (username,)
    cursor.execute(sql, val)
    db.commit()

    return f"Hello {username}, saved to database!"


@app.route("/users")
def users():

    sql = "SELECT * FROM users"
    cursor.execute(sql)

    all_users = cursor.fetchall()

    return render_template("users.html", users=all_users)


@app.route("/delete/<int:id>")
def delete(id):

    sql = "DELETE FROM users WHERE id = %s"
    val = (id,)

    cursor.execute(sql, val)
    db.commit()

    flash("User deleted successfully")

    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)