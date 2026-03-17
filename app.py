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

    flash(f"Hello {username}, saved to database")   #this f help to put value inside {}
    return redirect("/form")
    # return f"Hello {username}, saved to database!"


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


@app.route("/edit/<int:id>")
def edit(id):

    sql = "Select * from users where id = %s"
    val = (id,)

    cursor.execute(sql, val)
    user = cursor.fetchone()

    return render_template("edit.html", user = user)


@app.route("/update/<int:id>", methods = ["POST"])
def update(id):

    username = request.form["username"]
    sql = "Update users Set username = %s where id = %s"
    val = (username, id)

    cursor.execute(sql, val)
    db.commit()

    flash("User Updated Successfully")
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)