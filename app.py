import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.route("/")
@login_required
def homepage():

    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Faltou o nome do user", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Faltou a password", 403)

        # Creating users table
        # CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
        
        # Query database for username
        users_db = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(users_db) != 1 or not check_password_hash(users_db[0]["hash"], request.form.get("password")):
            return apology("User e/ou password inválidas", 403)

        # Remember which user has logged in
        session["user_id"] = users_db[0]["id"]

        # Redirect user to home page
        if not session["user_id"]:
            return redirect("/login")

        return redirect('/')

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # dealing with the case of the user clicking
        # on the “register” button without filling in the inputs
        if not username and not password and not confirmation:
            return apology("Deve escolher um username, uma password e confirmar", 403)

        if not username:
            return apology("Deve escolher um nome de utilizador", 403)

        if not password:
            return apology("Deve escolher uma password", 403)

        if not confirmation:
            return apology("Deve confirmar a password escolhida", 403)

        # If all 3 inputs are met
        if password != confirmation:
            return apology("Sorry, the passwords do not match")

        hashed_password = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES(?,?)", username, hashed_password)
            flash("Bem-vindo")
        except:
            # table users phpLiteAdmin: CREATE UNIQUE INDEX username ON users (username);
            return apology("Desculpe, o nome de utilizador que escolheu já se encontra em uso")

        session["user_id"] = new_user

        # in login: session["user_id"] = rows[0]["id"]

        return redirect('/')

    else:
        return render_template("register.html")