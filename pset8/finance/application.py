import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get current user's available cash
    user_row = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
    current_cash = user_row[0]['cash']

    # Gets current user's stock possession from inventory table
    user_stocks = db.execute("SELECT * FROM inventory WHERE user_id = :user_id", user_id=session["user_id"])

    # Initialize stock data to store dictionary of stocks
    stock_data = []

    # Initialize total market value owned by user
    total_value = 0

    # Loop through each stock that user holds
    for stock in user_stocks:

        # Extract id, bought price, shares
        stock_id = stock['stock_id']
        quantity = stock['quantity']

        # Get the symbol, name from stocks table
        get_stock_symbol = db.execute("SELECT * FROM stocks WHERE id = :id", id=stock_id)
        symbol = get_stock_symbol[0]["symbol"]
        name = get_stock_symbol[0]["name"]

        # Lookup the symbol thru API and get current price
        stock = lookup(symbol)
        current_price = stock['price']

        # Compute market value
        market_value = quantity * current_price

        # Update total market value
        total_value += market_value

        table_stock = {
            "symbol": symbol,
            "name": name,
            "shares": quantity,
            "current_price": usd(current_price),
            "market_value": usd(market_value)
        }

        stock_data.append(table_stock)

    # Round total_value
    total_value = round(total_value, 2)

    # Grand total cash + market value of user-owned stocks
    grand_total = current_cash + total_value

    return render_template("index.html", cash=usd(current_cash), data=stock_data, total_value=usd(total_value), total=usd(grand_total))

@app.route("/settings")
@login_required
def settings():
    """Adjust settings of user"""

    # Gets user's username
    temp = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])
    username = temp[0]["username"]

    # Gets user's buy transactions
    temp = db.execute("SELECT COUNT(*) FROM transactions WHERE user_id = :user_id AND buy = 1", user_id=session["user_id"])
    buys = temp[0]["COUNT(*)"]

    # Gets user's sell transactions
    temp = db.execute("SELECT COUNT(*) FROM transactions WHERE user_id = :user_id AND buy = 0", user_id=session["user_id"])
    sells = temp[0]["COUNT(*)"]

    return render_template("settings.html", username=username, buys=buys, sells=sells)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST
    if request.method == "POST":
        # Get symbol in the form of dictionary
        stock = lookup(request.form.get("symbol"))

        # Check if None is returned from API
        if stock is None:
            return apology("invalid symbol")

        # Get number of shares to purchase
        shares = int(request.form.get("shares"))

        # Ensure share is a positive number
        if shares < 1:
            return apology("shares to purchase must be a positive number")

        # Get respective name, price and symbol
        symbol = stock['symbol']
        name = stock['name']
        price = float(stock['price'])

        # Get total USD amount to be purchased
        amount = price * shares

        # Fetch user's row
        rows = db.execute("SELECT * FROM users WHERE id = :id",
                          id=session["user_id"])

        # Get user's cash and balance after purchase
        user_cash = rows[0]["cash"]
        balance = user_cash - amount

        # Check if user's cash is sufficient
        if balance < 0:
            return apology("cash insufficient")

        # Query for current symbol
        symbol_row = db.execute("SELECT * FROM stocks WHERE symbol = :symbol", symbol=symbol)

        # If symbol is not in table, insert into the table
        if len(symbol_row) == 0:
            db.execute("INSERT INTO stocks (symbol, name) VALUES (:symbol, :name)",
                       symbol=symbol, name=name)

        # Query for symbol_id
        temp = db.execute("SELECT id FROM stocks WHERE symbol = :symbol", symbol=symbol)
        symbol_id = temp[0]["id"]

        # Record buy transaction
        db.execute("INSERT INTO transactions (user_id, stock_id, shares, price, buy) VALUES (:user_id, :stock_id, :shares, :price, :buy)",
                   user_id=session["user_id"], stock_id=symbol_id, shares=shares, price=price, buy=1)

        # Query for user's inventory to check if stock already exist
        inventory_check = db.execute("SELECT quantity FROM inventory WHERE user_id = :user_id AND stock_id IN (SELECT id FROM stocks WHERE symbol = :symbol)",
                                     user_id=session["user_id"],
                                     symbol=symbol)

        # Add if stock is not in inventory
        if len(inventory_check) == 0:
            db.execute("INSERT INTO inventory (user_id, stock_id, quantity) VALUES (:user_id, :stock_id, :quantity)",
                       user_id=session["user_id"],
                       stock_id=symbol_id,
                       quantity=shares)

        # Update if stock already in inventory
        else:

            # Get current quantity and update with new shares
            current_quantity = int(inventory_check[0]["quantity"])
            current_quantity += shares

            # Update inventory with new quantity
            db.execute("UPDATE inventory SET quantity = :new_quantity WHERE user_id = :user_id AND stock_id = :stock_id",
                       new_quantity=current_quantity,
                       user_id=session["user_id"],
                       stock_id=symbol_id)

        # Update user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=balance, user_id=session["user_id"])

        return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Query current user's transactions
    user_transactions = db.execute("SELECT * FROM transactions AS t JOIN stocks AS s ON t.stock_id = s.id WHERE user_id = :user_id",
                                   user_id=session["user_id"])

    # Apply usd function to each price
    for transaction in user_transactions:
        transaction["price"] = usd(transaction["price"])

    return render_template("history.html", transactions=user_transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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

    # User reached route via POST
    if request.method == "POST":
        # Get symbol in the form of dictionary
        stock = lookup(request.form.get("symbol"))

        # Check if None is returned from API
        if stock is None:
            return apology("invalid symbol")

        # Get respective name, price and symbol
        name = stock['name']
        price = usd(stock['price'])
        symbol = stock['symbol']

        # Return quoted symbol
        return render_template("quoted.html", name=name, price=price, symbol=symbol)

    # User reached route via GET
    else:
        return render_template("quote.html")

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit some cash."""

    # User reached route via POST
    if request.method == "POST":
        # Get amount to be deposited
        deposit = float(request.form.get("deposit"))

        # Query for user's current cash
        temp = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        current_cash = temp[0]["cash"]

        # Update cash in memory
        current_cash += deposit

        # Update cash in database
        db.execute("UPDATE users SET cash = :current_cash WHERE id = :user_id",
                   current_cash=current_cash,
                   user_id=session["user_id"])

        return redirect("/")

    # User reached route via GET
    else:
        return render_template("deposit.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (submitting register)
    if request.method == "POST":

        # Get username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Ensure password and password confirmation is the same
        elif password != request.form.get("confirmation"):
            return apology("passwords don't match", 403)

        # Query database to check if username already exist
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Checks if there is an existing user with same username
        if len(rows) != 0:
            return apology("username already exist", 403)

        # Inserts registrant into table
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=username, hash=generate_password_hash(password))

        # Query database to ask for user id
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (get to registration page)
    else:
        return render_template("register.html")

@app.route("/verify", methods=["GET", "POST"])
@login_required
def verify():
    """Verifies user that wants to change password"""

    # User reached route via POST (submitting register)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        # Ensure password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("password is incorrect", 403)

        return redirect("/reset")

    # User reached route via GET (get to registration page)
    else:
        return render_template("verify.html")

@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    """Allows user to change password"""

    # User reached route via POST (submitting register)
    if request.method == "POST":

        # Get password
        password = request.form.get("password")

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 403)

        # Ensure password and password confirmation is the same
        elif password != request.form.get("confirmation"):
            return apology("passwords don't match", 403)

        # Update new password
        db.execute("UPDATE users SET hash = :new_hash WHERE id = :user_id",
                   new_hash=generate_password_hash(password),
                   user_id=session["user_id"])

        return redirect("/")

    # User reached route via GET (get to registration page)
    else:
        return render_template("reset.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        # To be sold
        symbol_sell = request.form.get("symbol")
        shares_sell = int(request.form.get("shares"))

        # Check user's inventory
        inventory_check = db.execute("SELECT * FROM inventory WHERE user_id = :user_id AND stock_id IN (SELECT id FROM stocks WHERE symbol = :symbol_sell)",
                                    user_id=session["user_id"],
                                    symbol_sell=symbol_sell)
        # Store stock id in memory
        stock_id_sell = inventory_check[0]["stock_id"]

        # Get shares owned by user
        shares_owned = int(inventory_check[0]["quantity"])
        shares_left = shares_owned - shares_sell

        # Check if shares to be sold is more than available
        if shares_left < 0:
            return apology("not enough shares", 403)

        # Update user's share if shares left is not 0
        if shares_left != 0:
            db.execute("UPDATE inventory SET quantity = :shares_left WHERE user_id = :user_id AND stock_id IN (SELECT id FROM stocks WHERE symbol = :symbol_sell)",
                       shares_left = shares_left,
                       user_id=session["user_id"],
                       symbol_sell=symbol_sell)

        # Remove the stock from user's row if shares left is 0
        else:
            db.execute("DELETE FROM inventory WHERE user_id = :user_id AND stock_id IN (SELECT id FROM stocks WHERE symbol = :symbol_sell)",
                       user_id=session["user_id"],
                       symbol_sell=symbol_sell)

        # Get symbol to be sold's latest price
        stock = lookup(symbol_sell)
        current_price = float(stock['price'])

        # Record sell transaction
        db.execute("INSERT INTO transactions (user_id, stock_id, shares, price, buy) VALUES (:user_id, :stock_id, :shares, :price, :buy)",
                   user_id=session["user_id"],
                   stock_id=stock_id_sell,
                   shares=shares_sell,
                   price=current_price,
                   buy=0)

        # Total to be sold
        total_sell = round(current_price * shares_sell, 2)

        # Queries for user's current cash and update cash
        user_row = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        current_cash = float(user_row[0]["cash"])
        current_cash += total_sell
        db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id",
                   new_cash=current_cash, user_id=session["user_id"])

        return redirect("/")

    # User reached route via GET
    else:
        # Get all stocks that user have
        symbol_rows = db.execute("SELECT symbol FROM inventory AS i JOIN stocks AS s ON i.stock_id = s.id WHERE i.user_id = :user_id",
                          user_id=session["user_id"])

        return render_template("sell.html", symbol_rows=symbol_rows)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
