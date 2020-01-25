import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import random

# import functions from helpers.py
from helpers import apology, login_required, change_password, change_username, change_discription


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
    """Checks if image file has allowed extension"""

    # Return false if filename has no dot
    if not "." in filename:
        return False

    # Get file extension
    ext = filename.rsplit(".", 1)[1]

    # Return true if file extension is allowed
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    """Checks if image is not too large"""

    # Return true if image is not larger then set maximum
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


# Remove print statements
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """Upload studyspot"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # If a image was uploaded
        if request.files:

            # if "filesize" in request.cookies:

                # if not allowed_image_filesize(request.cookies["filesize"]):
                #     print("Filesize exceeded maximum limit")
                #     return redirect(request.url)

            # Get image file
            image = request.files["image"]

            # If file has no name
            if image.filename == "":
                # print("No filename")
                return redirect(request.url)

            # If image is allowed
            if allowed_image(image.filename):

                filename = secure_filename(image.filename)
                # print(filename)

                # Save image
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                # print("Image saved")

                # Path to image file
                path = "static/posts/" + filename

                # Insert path to file in the database
                db.execute("INSERT INTO uploads (id, discription, path, title, street, postal, city, number) VALUES (:id, :discription, :path, :title, :street, :postal, :city, :number)", id=session.get("user_id"),
                discription=request.form.get("discription"), path=path, title=request.form.get("place name"), street=request.form.get("street"), postal=request.form.get("postal"), city=request.form.get("city"), number=request.form.get("number"))

                # Redirect to upload.html
                return redirect(request.url)

            # If image is not allowed redirect to upload.html
            else:
                # print("That file extension is not allowed")
                return redirect(request.url)

        # If user didnt upload a picture
        else:
            return apology("Upload a picture of the studyspot")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("upload.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change user settings"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get values from form
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

        # Changes username
        if request.form.get("username"):
            # Username already exists
            if len(db.execute("SELECT * FROM users WHERE username = :username", username=username)) != 0:
                return apology("username already exists")
            change_username(username, user_id)

        # Changes password
        if request.form.get("password"):
            # Check if password meets restrictions
            if not any(char.isdigit() for char in password):
                return apology("password must contain number")
            change_password(password, confirmation, user_id)

        # Changes discription
        if request.form.get("discription"):
            change_discription(discription, user_id)


        # Changes profile picture
        if request.files:

            # if "filesize" in request.cookies:

                # if not allowed_image_filesize(request.cookies["filesize"]):
                #     print("Filesize exceeded maximum limit")
                #     return redirect(request.url)

            # Get image file
            image = request.files["image"]

            # If image has no name
            if image.filename == "":
                # print("No filename")
                return redirect(request.url)

            # If image is allowed
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                # print(filename)

                # Save image
                image.save(os.path.join(app.config["PROFILE_UPLOADS"], filename))

                # print("Image saved")
                # Path to image file
                path = "static/profile/" + filename

                # Update path of profile picture in database
                db.execute("UPDATE users SET image = :image WHERE id=:user_id", user_id=session.get("user_id"), image=path)

                # Redirect to settings.html
                return redirect(request.url)

            else:
                # print("That file extension is not allowed")
                return redirect(request.url)

        # Redirect to settings.html
        return redirect(request.url)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")


@app.route("/")
@login_required
def profile():
    """Show profile page"""

    # Get user information
    user_id = session.get("user_id")
    discriptions = db.execute("SELECT discription FROM users WHERE id=:user_id", user_id=user_id)
    discription = discriptions[0]["discription"]
    usernames = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=user_id)
    username = usernames[0]["username"]
    posts = db.execute("SELECT path, postnumber FROM uploads WHERE id=:user_id", user_id=user_id)
    picture = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=user_id)
    followers = db.execute("SELECT userid FROM follow WHERE followid=:followid", followid=user_id)
    following = db.execute("SELECT followid FROM follow WHERE userid=:userid", userid=user_id)
    # likes = db.execute("SELECT postid FROM likes")
    # likes_list = []
    #for like in likes:
    #    likes_list

    # Initialize ...
    followerslist = []
    followinglist = []
    iddict = {}
    post_dict = {}

    #
    if posts:
        for post in posts:
            likes = db.execute("SELECT postid FROM likes WHERE postid=:postid", postid=post["postnumber"])
            print(likes)
            post_dict[post["postnumber"]] = (post["path"], len(likes))

    #
    if followers:
        for follower in followers:
            f = follower["userid"]
            name = db.execute("SELECT username FROM users WHERE id=:id", id=f)
            followerslist.append(name)
            iddict[name[0]["username"]] = f

    #
    if following:
        for followin in following:
            fol = followin["followid"]
            names = db.execute("SELECT username FROM users WHERE id=:id", id=fol)
            followinglist.append(names)
            iddict[names[0]["username"]] = fol

    # Render profile page
    return render_template("profile.html", discription=discription, username=username, picture=picture, followerslist=followerslist, followinglist=followinglist, iddict=iddict, post_dict=post_dict)

@app.route("/<int:user>")
@login_required
def userprofile(user):
    """Show profile page"""

    # Get user information
    follow_id = user
    discriptions = db.execute("SELECT discription FROM users WHERE id=:user_id", user_id=follow_id)
    discription = discriptions[0]["discription"]
    usernames = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=follow_id)
    username = usernames[0]["username"]
    posts = db.execute("SELECT path, postnumber FROM uploads WHERE id=:user_id", user_id=follow_id)
    picture = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=follow_id)
    following = db.execute("SELECT followid FROM follow WHERE userid=:user_id AND followid=:followid", user_id=session.get("user_id"), followid=follow_id)

    # False if user follows user already
    if following:
        bool_follow = False
    else:
        bool_follow = True

    # False if user looks at his own page
    if user == session.get("user_id"):
        bool_user = False
    else:
        bool_user = True

    #
    followers = db.execute("SELECT userid FROM follow WHERE followid=:followid", followid=follow_id)
    following = db.execute("SELECT followid FROM follow WHERE userid=:userid", userid=follow_id)

    #
    followerslist = []
    followinglist = []
    iddict = {}
    post_dict = {}

    #
    if posts:
        for post in posts:
            post_dict[post["postnumber"]] = post["path"]

    #
    if followers:
        for follower in followers:
            f = follower["userid"]
            name = db.execute("SELECT username FROM users WHERE id=:id", id=f)
            followerslist.append(name)
            iddict[name[0]["username"]] = f

    #
    if following:
        for followin in following:
            fol = followin["followid"]
            names = db.execute("SELECT username FROM users WHERE id=:id", id=fol)
            followinglist.append(names)
            iddict[names[0]["username"]] = fol

    # Render profile page
    return render_template("profile.html", discription=discription, username=username, posts=posts, picture=picture, bool_user=bool_user, user_id=follow_id, bool_follow=bool_follow
    , followerslist=followerslist, followinglist=followinglist, iddict=iddict, post_dict=post_dict)


@app.route("/follow/<int:followid>", methods=["POST"])
@login_required
def follow(followid):
    """Lets user follow another user"""

    user_id = session.get("user_id")
    db.execute("INSERT INTO follow (followid, userid) VALUES(:followid, :userid)", followid=followid, userid=user_id)
    return True

@app.route("/unfollow/<int:followid>", methods=["POST"])
@login_required
def unfollow(followid):
    """Let user unffolw another user"""

    user_id = session.get("user_id")
    db.execute("DELETE FROM follow WHERE followid=:followid AND userid=:userid", followid=followid, userid=user_id)
    return True


@app.route("/following")
@login_required
def following():
    """Show followingpage"""

    # Get user_id
    user_id = session.get("user_id")

    # Get users which the user follows
    following = db.execute("SELECT followid FROM follow WHERE userid=:userid", userid=user_id)

    # Get all posts from following users
    if following:
        postnumbers = []
        for user in following:
            postnumbers.append(db.execute("SELECT postnumber FROM uploads WHERE id=:user_id", user_id=user['followid']))

        # Store all posts of all the people the user is following in posts
        posts = []
        for user in postnumbers:
            # for every post the user has made
            for post in user:
                posts.append(db.execute("SELECT path FROM uploads WHERE postnumber=:postnumber", postnumber=post['postnumber']))

        numberset = set()
        for postnumber in postnumbers:
            numberset.add(postnumber[0]["postnumber"])
        number = random.choice(tuple(numberset))

    # render html page
    return render_template("following.html", post=posts[0], number=number)


@app.route("/favorites")
@login_required
def favorites():
    """Show favoritespage"""

    # Get user_id
    user_id = session.get("user_id")

    # Get favorite posts of the user
    favorites = db.execute("SELECT postid FROM favorites WHERE favuserid=:favuserid", favuserid=user_id)

    # If user has favorite posts
    if favorites:
        #
        posts = []
        numberset = set()
        for post in favorites:
            posts.append(db.execute("SELECT path FROM uploads WHERE postnumber=:postnumber", postnumber=post['postid']))
            numberset.add(post["postid"])

        # Choose a random post
        number = random.choice(tuple(numberset))

        # render html page
        return render_template("favorites.html", post=posts[0], number=number)

    else:
        return apology("You dont have any favorite posts yet")


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
        db.execute("INSERT INTO users (username, hash, image, discription) VALUES (:username, :hash, :image, :discription)", username=username, hash=hash, image="static/profile/grumpy.png", discription="Add a discription in settings")

        # Redirect to /login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/discover")
@login_required
def discover():
    """"""

    #
    post_number = db.execute("SELECT postnumber FROM uploads")
    numberset = set()
    for numbers in post_number:
        numberset.add(numbers["postnumber"])
    number = random.choice(tuple(numberset))
    post = db.execute("SELECT path FROM uploads WHERE postnumber=:postnumber", postnumber=number)
    user = db.execute("SELECT id FROM uploads WHERE postnumber=:postnumber", postnumber=number)
    poster_id = user[0]["id"]
    username = db.execute("SELECT username FROM users WHERE id=:id", id=poster_id)
    likes = len(db.execute("SELECT postid FROM likes WHERE postid=:postid", postid=number))


    liking = db.execute("SELECT postid FROM likes WHERE likerid=:likerid AND postid=:postid", likerid = session.get("user_id"), postid=number)

    # False if user already liked this post
    if liking:
        bool_like= False
    else:
        bool_like = True
    return render_template("discover.html", post=post, number=number, bool_like=bool_like, username=username, likes=likes)


@app.route("/info/<int:post_id>")
@login_required
def info(post_id):
    """"""
    number = post_id
    titles = db.execute("SELECT * FROM uploads WHERE postnumber=:postnumber", postnumber = number)
    user_id = titles[0]["id"]
    name = db.execute("SELECT username FROM users WHERE id=:id", id=user_id)
    liking = db.execute("SELECT postid FROM likes WHERE likerid=:likerid AND postid=:postid", likerid = session.get("user_id"), postid=number)
    # False if user already liked this post
    if liking:
        bool_like= False
    else:
        bool_like = True
    #
    return render_template("info.html",titles=titles, number=number, name=name, bool_like=bool_like)


@app.route("/about")
def about():
    return render_template("about.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


@app.route("/like/<int:postid>", methods=["POST"])
@login_required
def like(postid):
    """Allowing user to like a post"""
    print("aad")
    likerid = session.get("user_id")
    db.execute("INSERT INTO likes (postid, likerid) VALUES(:postid, :likerid)", postid=postid, likerid=likerid)

    return redirect("/discover")


@app.route("/unlike/<int:postid>", methods=["POST"])
@login_required
def unlike(postid):
    """Allowing user to unlike a post they liked before"""
    likerid = session.get("user_id")
    db.execute("DELETE FROM likes WHERE postid=:postid AND likerid=:likerid", postid=postid, likerid=likerid)

    return redirect("/discover")


@app.route("/favorite/<int:post_id>", methods=["POST"])
@login_required
def favorite(post_id):
    """Add post to favorites"""
    print("maat")
    # Get id of the user
    user_id = session.get("user_id")

    # Add post to user's favorites
    db.execute("INSERT INTO favorites (postid, favuserid) VALUES (:postid, :favuserid)", postid=post_id, favuserid=user_id)

    return redirect("/")