import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import random

from helpers import apology, login_required, lookup, usd, format_date, format_hour

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_transactions = db.execute("SELECT symbol, SUM(shares) AS total_shares, price, SUM(shares * price) AS total_value\
        FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0 ORDER BY symbol ASC", session["user_id"])

    current_cash_db = db.execute(
        "SELECT users.cash FROM users WHERE users.id = ?", session["user_id"])

    current_cash = current_cash_db[0]["cash"]

    stocks_total_db = db.execute(
        "SELECT SUM(shares * price) AS st FROM transactions WHERE user_id = ?", session["user_id"])
    stocks_total = stocks_total_db[0]["st"]
    if stocks_total == None:
        stocks_total = 0

    grand_total = stocks_total + current_cash

    return render_template("index.html", user_transactions=user_transactions, current_cash=current_cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # dealing with the case of the user clicking
        # on the “buy” button without filling in the inputs
        if not symbol and not shares:
            return apology("You must give a symbol and the number of shares")

        stock = lookup(symbol.upper())
        if not stock:
            return apology("The symbol does not exist")

        try:
            shares = int(shares)
        except:
            return apology("You must give a correct number of shares")

        if shares <= 0:
            return apology("The number of shares are incorrect or is missing")

        current_user_cash_db = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        current_user_cash = current_user_cash_db[0]["cash"]

        total_purchase = stock["price"] * float(shares)

        cash_now = current_user_cash - total_purchase

        if cash_now < 0:
            return apology("Your balance does not allow this transaction")

        # updating cash in users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   cash_now, session["user_id"])

        # formatting
        date = format_date(datetime.datetime.now())
        hour = format_hour(datetime.datetime.now())

        shares = float(shares)

        # updating transaction table
        db.execute("INSERT INTO transactions (user_id,symbol,shares,price,total_purchase,date,hour,type_transac) \
            VALUES(?,?,?,?,?,?,?,?)", session["user_id"], stock["symbol"], shares, stock["price"], total_purchase,
                   date, hour, "BOUGHT")

        flash("Bought!")

        return redirect('/')


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_history = db.execute("SELECT symbol,shares,price,total_purchase,date,hour,type_transac FROM transactions\
        WHERE user_id = ?", session["user_id"])

    return render_template("history.html", user_history=user_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        if not session["user_id"]:
            return redirect("/login")
        flash(f"Welcome, {request.form.get("username")}!")

        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:

        symbol = request.form.get("symbol")

        # dealing with the case of the user clicking
        # on the “quote" button without filling in the input
        if not symbol:
            return apology("You must give a symbol")

        stock = lookup(symbol.upper())
        if not stock:
            return apology("Sorry, the stock quote does not exist")

        price = stock["price"]

        return render_template("quoted.html", price=price, stock=stock)


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
            return apology("Must choose username, password and confirmation")

        if not username:
            return apology("Must choose username")

        if not password:
            return apology("Must choose password")

        if not confirmation:
            return apology("Must give confirmation")

        # If all 3 inputs are met
        if password != confirmation:
            return apology("Sorry, the passwords do not match")

        hashed_password = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES(?,?)", username, hashed_password)
            flash(f"Welcome, {username}!")
        except:
            # table users phpLiteAdmin: CREATE UNIQUE INDEX username ON users (username);
            return apology("Sorry, the username already exists. Please, choose another one")

        session["user_id"] = new_user

        # in login: session["user_id"] = rows[0]["id"]

        return redirect('/')

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        active_symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol\
            HAVING SUM(shares) > 0 ORDER BY symbol", session["user_id"])

        return render_template("sell.html", symbols=[row["symbol"] for row in active_symbols])
        # symbols will be a list only with the user symbols

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # dealing with the case of the user clicking
        # on the “sell” button without filling in the input
        if not shares:
            return apology("You must give the number of shares")

        try:
            shares = int(shares)
        except:
            return apology("You must give a correct number of shares")

        shares_now = db.execute("SELECT SUM(shares) AS total_shares FROM transactions \
            WHERE transactions.user_id = ? AND transactions.symbol = ?",
                                session["user_id"], symbol)

        # dealing with "shares" errors
        if not shares:
            return apology("You must give the number of shares")

        if int(shares) > shares_now[0]["total_shares"]:
            return apology("You do not have enough shares to sell")

        # updating cash in users table
        current_user_cash_db = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        current_user_cash = current_user_cash_db[0]["cash"]

        stock = lookup(symbol)

        total_purchase = stock["price"] * shares
        cash_now = current_user_cash + total_purchase

        if float(cash_now) <= 0:
            return apology("Your balance does not allow this transaction")
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   cash_now, session["user_id"])

        # formatting
        date = format_date(datetime.datetime.now())
        hour = format_hour(datetime.datetime.now())

        # updating transaction table
        db.execute("INSERT INTO transactions (user_id,symbol,shares,price,total_purchase,date,hour,type_transac)\
            VALUES(?,?,?,?,?,?,?,?)", session["user_id"], stock["symbol"], (-1)*int(shares), stock["price"],
                   total_purchase, date, hour, "SOLD")

        flash("Sold!")

        return redirect("/")


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to user account."""

    if request.method == "GET":
        # Create a list with payment methods
        payment_methods = ["Paypal", "Apple Pay", "Google Pay", "Amazon Pay",
                           "Bank Transfer", "Credit Card", "Bitcoin"]

        return render_template("addcash.html", payment_methods=payment_methods)

    else:
        add_cash = request.form.get("add_cash")
        payment_chosen = request.form.get("payment")

        if not payment_chosen:
            return apology("You must choose a payment method")

        if not add_cash:
            return apology("You must give an amount")

        if payment_chosen and add_cash:
            # updating the addcashhistory table in database
            # Assume “Failure” before confirming a possible “Success”
            db.execute("INSERT INTO addcashhistory (user_id,method,addcash,observation) \
            VALUES(?,?,?,?)", session["user_id"], payment_chosen, add_cash, "Failure")

            return redirect('/confadd')


@app.route("/confadd", methods=["GET", "POST"])
@login_required
def confadd():

    if request.method == "GET":
        random_code = random.randrange(0, 100000, 5)
        flash(f"Code from text message: {random_code}")
        return render_template("confadd.html", random_code=random_code)

    else:
        confirmation_code = request.form.get("confirmation_code")
        random_code = request.form.get("random_code")

        if not confirmation_code:
            return apology("You have to enter the code you received by text message")

        if confirmation_code != random_code:
            flash("Wrong code! Please, repeat the process")
            return redirect('/addcash')

        # identify the last "add cash" id
        last_add_cash_id_db = db.execute("SELECT id FROM addcashhistory WHERE user_id = ? \
            ORDER BY id DESC LIMIT 1", session["user_id"])
        last_add_cash_id = last_add_cash_id_db[0]["id"]

        # updating cash in users table and addcashhistory table (With "Success")
        old_cash_db = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        old_cash = old_cash_db[0]["cash"]

        add_cash_db = db.execute("SELECT addcash FROM addcashhistory WHERE user_id = ? \
            AND id = ? ", session["user_id"], last_add_cash_id)
        add_cash = add_cash_db[0]["addcash"]

        update_cash = int(old_cash) + int(add_cash)

        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   update_cash, session["user_id"])
        db.execute("UPDATE addcashhistory SET observation = ? WHERE id = ? \
            AND user_id = ?", "Success", last_add_cash_id, session["user_id"])

        flash(f"You add ${add_cash} to your account! Now you have ${
              update_cash} available")

        return redirect('/')
