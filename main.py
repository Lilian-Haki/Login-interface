from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import psycopg2

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
conn = psycopg2.connect(
    user="postgres", password="lilian", host="127.0.0.1", port="5432", database="login"
)
cur = conn.cursor()
app.config["SECRET_KEY"] = "#lilian"

# Intialize MySQL
mysql = MySQL(app)


@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cur.execute(
            "select * from accounts where username=%s and password=%s",
            (username, password),
        )
        record = cur.fetchone()
        if record:
            session["loggedin"] = True
            session["username"] = record[1]
            # return redirect(url_for("sign_up"))
            return "WELCOME"
    else:
        msg = "Incorrect username/password.Try again!"
    return render_template("login.html", msg=msg)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        cur.execute(
            "INSERT INTO accounts (username,password,email) VALUES(%s,%s,%s)",
            (user_name, password, email),
        )
        conn.commit()
        return redirect(url_for("/"))
    else:
        return render_template("register.html")


# @app.route("/sign_up", methods=["GET", "POST"])
# def dashboard():


@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    # Redirect to login page
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
