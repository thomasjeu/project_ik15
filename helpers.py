import requests
import urllib.parse
import os

from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def change_password():
    """ Changes password """


    # Ensure password was submitted
    if not request.form.get("password"):
        return apology("must provide password")

    # Password confirmation
    elif not request.form.get("confirmation"):
        return apology("must provide confirmation of password")

    # Check if passwords are similair
    elif request.form.get("password") != request.form.get("confirmation"):
        return apology("passwords must be the same")

    # Hashes the password
    password = request.form.get("password")
    hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    # Update password in database
    user_id = session.get("user_id")
    db.execute("UPDATE users SET hash=:hash WHERE id=:user_id", user_id=user_id, hash=hash)

    # Redirt to index
    return redirect("/settings")