import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

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


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    print("maat")
    if request.method == "POST":
        print("gozer")
        if request.files:
            print("aad")
            print(request.cookies)
            # if "filesize" in request.cookies:

                # if not allowed_image_filesize(request.cookies["filesize"]):
                #     print("Filesize exceeded maximum limit")
                #     return redirect(request.url)

            image = request.files["image"]
            print("hoi")
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            print("hoii")
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                print(filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                print("Image saved")
                path = "static/posts/" + filename

                db.execute("INSERT INTO uploads (id, discription, path, title, street, postal, city) VALUES (:id, :discription, :path, :title, :street, :postal, :city)", id=session.get("user_id"),
                discription=request.form.get("discription"), path=path, title=request.form.get("place name"), street=request.form.get("street"), postal=request.form.get("postal"), city=request.form.get("city"))

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    print("yo")
    return render_template("upload.html")


@app.route("/twodiscover", methods=["GET", "POST"])
@login_required
def twodiscover():
    return render_template("twodiscover.html")



@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        username = request.form.get("username")
        confirmation = request.form.get("confirmation")
        discription = request.form.get("discription")
        password = request.form.get("password")
        user_id = session.get("user_id")


        # Check if passwords are similair
        if (password != confirmation):
            return apology("passwords must be the same")

        # Check if discription is not too long
        if len(discription) > 400:
            return apology("discription is too long")

        if request.form.get("username"):
            # Username already exists
            if len(db.execute("SELECT * FROM users WHERE username = :username", username=username)) != 0:
                return apology("username already exists")
            changeusername(username, user_id)

        if request.form.get("password"):
            # Check if password meets restrictions
            if not any(char.isdigit() for char in password):
                return apology("password must contain number")
            changepassword(password, confirmation, user_id)

        if request.form.get("discription"):
            changediscription(discription, user_id)


        if request.files:
            print("aad")
            print(request.cookies)
            # if "filesize" in request.cookies:

                # if not allowed_image_filesize(request.cookies["filesize"]):
                #     print("Filesize exceeded maximum limit")
                #     return redirect(request.url)

            image = request.files["image"]
            print("hoi")
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            print("hoii")
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                print(filename)
                image.save(os.path.join(app.config["PROFILE_UPLOADS"], filename))

                print("Image saved")
                path = "static/profile/" + filename

                db.execute("UPDATE users SET image = :image WHERE id=:user_id", user_id=session.get("user_id"), image=path)

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)




        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")


@app.route("/")
@login_required
def profile():
    user_id = session.get("user_id")
    discriptions = db.execute("SELECT discription FROM users WHERE id=:user_id", user_id=user_id)
    discription = discriptions[0]["discription"]
    usernames = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=user_id)
    username = usernames[0]["username"]
    posts = db.execute("SELECT path FROM uploads WHERE id=:user_id", user_id=user_id)
    picture = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=user_id)

    return render_template("profile.html", discription=discription, username=username, posts=posts, picture=picture)

@app.route("/followingprofile")
@login_required
def followingprof():
    user_id = session.get("user_id")
    discriptions = db.execute("SELECT discription FROM users WHERE id=:user_id", user_id=user_id)
    discription = discriptions[0]["discription"]
    usernames = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=user_id)
    username = usernames[0]["username"]
    picture = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=user_id)
    return render_template("followingprofile.html", discription=discription, username=username, picture=picture)

@app.route("/followersprofile")
@login_required
def followersprof():
    """Followers as shown on profile"""
    user_id = session.get("user_id")
    discriptions = db.execute("SELECT discription FROM users WHERE id=:user_id", user_id=user_id)
    discription = discriptions[0]["discription"]
    usernames = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=user_id)
    username = usernames[0]["username"]
    picture = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=user_id)
    return render_template("followersprofile.html", discription=discription, username=username, picture=picture)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get username that the user would like to have
    username = request.args.get("username")

    # Check if username already exists in users
    rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)

    # return False if the username is unique else True
    if len(rows) != 0 or len(username) == 0:
        return jsonify(False)

    else:
        return jsonify(True)


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Username already exists
        elif len(db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))) != 0:
            return apology("username already exists")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Password confirmation
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation of password")

        # Ensure the passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must be the same")

        # Get username and password given by the user
        username = request.form.get("username")
        password = request.form.get("password")

        # Hashes the password
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Insert user into the database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)

        # Redirect to /login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/discover", methods=["GET", "POST"])
def discover():

    return render_template("discover.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
