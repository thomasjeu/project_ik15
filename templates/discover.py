import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from random import seed
from random import random


from helpers import apology, login_required, changepassword, changeusername, changediscription


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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///admin.db")

app.config["IMAGE_UPLOADS"] = "static/posts"
app.config["PROFILE_UPLOADS"] = "static/profile"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
# app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


@app.route("twodiscover")
@login_required
def twodiscover():
    number = request.cookies["postnumber"]
    print(number)
    user_id = session.get("user_id")

    titles = db.execute("SELECT title FROM users WHERE id=:user_id", user_id=user_id)
    title = titles[0]["title"]

    discriptions = db.execute("SELECT discription FROM uploads WHERE id=:user_id", user_id=user_id)
    discription = discriptions[0]["discription"]

    street_one = db.execute("SELECT street FROM uploads WHERE id=:user_id", user_id=user_id)
    street = street_one[0]["street"]

    postal_one = db.execute("SELECT postal FROM uploads WHERE id=:user_id", user_id=user_id)
    postal = postal_one[0]["postal"]

    city_one = db.execute("SELECT city FROM uploads WHERE id=:user_id", user_id=user_id)
    city = city_one[0]["city"]

    return render_template("twodiscover.html", discription=discription, title=title, street=street, postal=postal, city=city)


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False



# @app.route("/discover", methods=["GET"])
# @login_required
# def discover():

#     post_nummer = db.execute("SELECT postnumber FROM uploads WHERE id=:user_id", user_id=session.get("user_id"))
#     print(post_nummer)
#     seed(1)
#     for random in range(len(post_nummer)):
#         randomvalue = int(random())
#         print(randomvalue)
#     return render_template("discover.html")
