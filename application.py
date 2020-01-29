import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from os import listdir
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import random

# import functions from helpers.py
from helpers import apology, login_required, change_password, change_username, change_discription, fill_post_dict, user_information, is_following, is_user, liked_post, favo_post, user_information_users


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


@app.route("/")
@login_required
def profile():
    """ Show profile page """

    # Get user information
    user_id = session.get("user_id")
    discription, username, posts, picture, followers, following = user_information(user_id)

    # Initialize lists and dictionary
    followers_list, following_list = [], []
    id_dict, post_dict = {}, {}

    # If user has posts
    if posts:
        post_dict = fill_post_dict(posts)

    # If user has followers
    if followers:
        for follower in followers:
            name = db.execute("SELECT username FROM users WHERE id=:id", id=follower["user_id"])
            followers_list.append(name)
            id_dict[name[0]["username"]] = follower["user_id"]

    # If user follows users
    if following:
        for user in following:
            name = db.execute("SELECT username FROM users WHERE id=:id", id=user["follow_id"])
            following_list.append(name)
            id_dict[name[0]["username"]] = user["follow_id"]

    # Render profile page
    return render_template("profile.html", discription=discription, username=username, picture=picture, followerslist=followers_list, followinglist=following_list, iddict=id_dict, post_dict=post_dict)


@app.route("/<int:user_id>")
@login_required
def userprofile(user_id):
    """ Show profile page """

    # Get user information
    discription, username, posts, picture, followers, following = user_information_users(user_id)

    # False if user follows user already
    bool_follow = is_following(followers, session.get("user_id"))

    # False if user looks at his own page
    bool_user = is_user(user_id, session.get("user_id"))

    # Initialize lists and dictionary
    followers_list, following_list = [], []
    id_dict, post_dict = {}, {}

    # If user has posts
    if posts:
        post_dict = fill_post_dict(posts)

    # If user has followers
    if followers:
        for follower in followers:
            name = db.execute("SELECT username FROM users WHERE id=:id", id=follower["user_id"])
            followers_list.append(name)
            id_dict[name[0]["username"]] = follower["user_id"]

    # If user follows users
    if following:
        for user in following:
            name = db.execute("SELECT username FROM users WHERE id=:id", id=user["follow_id"])
            following_list.append(name)
            id_dict[name[0]["username"]] = user["follow_id"]

    # Render profile page
    return render_template("profile.html", discription=discription, username=username, posts=posts, picture=picture, bool_user=bool_user, user_id=user_id, bool_follow=bool_follow,
                           followerslist=followers_list, followinglist=following_list, iddict=id_dict, post_dict=post_dict)


@app.route("/about")
def about():
    """ Shows about page """
    return render_template("about.html")


@app.route("/check", methods=["GET"])
def check():
    """ Return true if username available, else false, in JSON format """

    # Get username that the user would like to have
    username = request.args.get("username")

    # Check if username already exists in users
    rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)

    # return False if the username is unique else True
    if len(rows) != 0 or len(username) == 0:
        return jsonify(False)

    else:
        return jsonify(True)


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    """ Deletes post from database """

    # Removes image from static/posts
    path = db.execute("SELECT path FROM uploads WHERE id=:id", id=post_id)
    os.remove(path[0]["path"])

    # Delete post from database and favorites related to the posts
    db.execute("DELETE FROM uploads WHERE id=:id", id=post_id)
    db.execute("DELETE FROM favorites WHERE post_id=:post_id", post_id=post_id)

    # Redirect to profile page
    return redirect("/")


@app.route("/discover")
@login_required
def discover():
    """ Let user discover studyspots """

    # Get post info
    posts = db.execute("SELECT id FROM uploads WHERE status=1")
    id_set = set()
    [id_set.add(post["id"]) for post in posts]
    post_id = random.choice(tuple(id_set))
    post = db.execute("SELECT path FROM uploads WHERE id=:id", id=post_id)
    user_id = db.execute("SELECT user_id FROM uploads WHERE id=:id", id=post_id)[0]["user_id"]
    username = db.execute("SELECT username FROM users WHERE id=:id", id=user_id)
    likes = len(db.execute("SELECT post_id FROM likes WHERE post_id=:post_id", post_id=post_id))

    # True if user didnt favorite the post
    bool_favo = favo_post(session.get("user_id"), post_id)

    # True if user didnt like the post
    bool_like = liked_post(session.get("user_id"), post_id)

    # Render discover.html
    return render_template("discover.html", post=post, number=post_id, bool_like=bool_like, username=username, likes=likes, bool_favo=bool_favo)


@app.route("/favorite/<int:post_id>", methods=["POST"])
@login_required
def favorite(post_id):
    """ Add post to favorites """

    # Get id of the user
    user_id = session.get("user_id")

    # If user already has max amount of favorites
    if len(db.execute("SELECT * FROM favorites WHERE user_id=:user_id", user_id=user_id)) >= 20:
        return apology("You already have the maximum amount of favorites")

    # Add post to user's favorites
    db.execute("INSERT INTO favorites (post_id, user_id) VALUES (:post_id, :user_id)", post_id=post_id, user_id=user_id)

    # Get the amount of favorites
    amount = len(db.execute("SELECT post_id FROM favorites WHERE post_id=:post_id", post_id=post_id))

    # Change status to hidden if post has 100 or more favorites
    if int(amount) > 49:
        db.execute("UPDATE uploads SET status=0 WHERE id=:post_id", post_id=post_id)

    # Redirect to favorites
    return redirect("/favorites")


@app.route("/favorites")
@login_required
def favorites():
    """ Show favoritespage """

    # Get user_id
    user_id = session.get("user_id")

    # Get post_ids in users favorite
    favorites = db.execute("SELECT post_id FROM favorites WHERE user_id=:user_id", user_id=user_id)

    # If user has favorite posts
    if favorites:

        # Get posts to be displayed
        posts = []
        for post in favorites:
            posts.append(db.execute("SELECT id, path, title  FROM uploads WHERE id=:id", id=post['post_id']))

        # render html page
        return render_template("favorites.html", posts=posts)

    # Return apology if user has no favorite posts
    else:
        return apology("You dont have any favorite posts yet")


@app.route("/follow/<int:follow_id>", methods=["POST"])
@login_required
def follow(follow_id):
    """ Lets user follow another user """

    user_id = session.get("user_id")
    db.execute("INSERT INTO follow (follow_id, user_id) VALUES(:follow_id, :user_id)", follow_id=follow_id, user_id=user_id)
    return redirect("/")


@app.route("/following")
@login_required
def following():
    """ Show followingpage """

    # Get user_id
    user_id = session.get("user_id")

    # Get users which the user follows
    following = db.execute("SELECT follow_id FROM follow WHERE user_id=:user_id", user_id=user_id)

    # Get all posts from following users
    if following:
        post_ids = []
        for user in following:
            post_ids.append(db.execute("SELECT id FROM uploads WHERE user_id=:user_id AND status=1", user_id=user['follow_id']))

        # Store all posts of all the people the user is following in posts
        posts = []
        for post_id in post_ids:
            # for every post the user has made
            for post in post_id:
                posts.append(db.execute("SELECT id, path, title FROM uploads WHERE id=:id AND status=1", id=post['id']))

        # render html page
        return render_template("following.html", posts=posts)

    # Return apology if the user is not following anyone with posts
    else:
        return apology("You are not following anyone who have posts")


@app.route("/info/<int:post_id>")
@login_required
def info(post_id):
    """ Show user extra information about studyspot """

    # Get user_id
    user_id = session.get("user_id")

    # Get all information from the post
    titles = db.execute("SELECT * FROM uploads WHERE id=:id", id=post_id)
    user = titles[0]["user_id"]
    name = db.execute("SELECT username FROM users WHERE id=:id", id=user)

    # True if user didnt favorite the post
    bool_favo = favo_post(session.get("user_id"), post_id)

    # True if user didnt like the post
    bool_like = liked_post(session.get("user_id"), post_id)

    # False if user looks at his own post
    bool_user = is_user(user, user_id)

    # Render info page
    return render_template("info.html", titles=titles, number=post_id, name=name, bool_like=bool_like, user=user, bool_user=bool_user, bool_favo=bool_favo)


@app.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like(post_id):
    """ Allowing user to like a post """

    # Add like to database
    user_id = session.get("user_id")
    db.execute("INSERT INTO likes (post_id, user_id) VALUES(:post_id, :user_id)", post_id=post_id, user_id=user_id)

    # Redirect to info page from the post
    return redirect(url_for("info", post_id=post_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

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
    """ Log user out """

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """

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
        db.execute("INSERT INTO users (username, hash, image, discription) VALUES (:username, :hash, :image, :discription)", username=username,
                   hash=hash, image="static/profile/grumpy.png", discription="Add a discription in settings and change your profile picture")

        # Redirect to /login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """ Change user settings """

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

            # Get image file
            image = request.files["image"]

            # If image has no name
            if image.filename == "":
                return redirect("/")

            # Get all imagenames existing already
            image_names = [name for name in listdir("static/profile/")]

            if image.filename in image_names:
                return apology("Please change the name of the image")

            # If image is allowed
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)

                # Save image
                image.save(os.path.join(app.config["PROFILE_UPLOADS"], filename))

                # Path to image file
                path = "static/profile/" + filename

                # Delete previous image if it is not grumpy
                previous_path = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=session.get("user_id"))
                if previous_path != "static/profile/grumpy.png":
                    os.remove(previous_path[0]["image"])

                # Update path of profile picture in database
                db.execute("UPDATE users SET image=:image WHERE id=:user_id", user_id=session.get("user_id"), image=path)

                # Redirect to profile.html
                return redirect("/")

        # Redirect to profile.html
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")


@app.route("/unfavorite/<int:post_id>", methods=["POST"])
@login_required
def unfavorite(post_id):
    """ Allowing user to unfavorite a post they favorited before """

    # Delete favorite from database that user unfavorite
    user_id = session.get("user_id")
    db.execute("DELETE FROM favorites WHERE post_id=:post_id AND user_id=:user_id", post_id=post_id, user_id=user_id)

    # Get the amount of favorites
    amount = len(db.execute("SELECT post_id FROM favorites WHERE post_id=:post_id", post_id=post_id))

    # Change status to hidden if post has 50 or more favorites
    if int(amount) < 50:
        db.execute("UPDATE uploads SET status=1 WHERE id=:post_id", post_id=post_id)

    # Redirect to info page of the post
    return redirect(url_for("info", post_id=post_id))


@app.route("/unfollow/<int:follow_id>", methods=["POST"])
@login_required
def unfollow(follow_id):
    """ Let user unfollow another user """

    # Delete follow from database
    user_id = session.get("user_id")
    db.execute("DELETE FROM follow WHERE follow_id=:follow_id AND user_id=:user_id", follow_id=follow_id, user_id=user_id)

    # Redirect to profile page
    return redirect("/")


@app.route("/unlike/<int:post_id>", methods=["POST"])
@login_required
def unlike(post_id):
    """ Allowing user to unlike a post they liked before """

    # Unlike the post
    user_id = session.get("user_id")
    db.execute("DELETE FROM likes WHERE post_id=:post_id AND user_id=:user_id", post_id=post_id, user_id=user_id)

    # Redirect to info page of the post
    return redirect(url_for("info", post_id=post_id))


# TODO: Filter wrong user input
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """ Upload studyspot """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get form values
        discription = request.form.get("discription")
        title = request.form.get("place name")
        street = request.form.get("street")
        postal = request.form.get("postal")
        city = request.form.get("city")
        number = request.form.get("number")

        # Return apologies if one of the form fields wasnt filled in
        if not discription:
            return apology("Must provide a discription")

        if not title:
            return apology("Must provide the name of the place")

        if not street:
            return apology("Must provide a streetname")

        if not postal:
            return apology("Must provide a postalcode")

        if not city:
            return apology("Must provide a city or town name")

        if not number:
            return apology("Must provide a street number")

        # If a image was uploaded
        if request.files:

            # Get image file
            image = request.files["image"]

            # If file has no name
            if image.filename == "":
                return apology("imagefile has no name")

            # Get all imagenames existing already
            image_names = [name for name in listdir("static/posts/")]

            if image.filename in image_names:
                return apology("Please change the name of the image")

            # If image is allowed
            if allowed_image(image.filename):

                filename = secure_filename(image.filename)

                # Save image
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                # Path to image file
                path = "static/posts/" + filename

                # Insert path to file in the database
                db.execute("INSERT INTO uploads (discription, path, title, street, postal, city, user_id, number) VALUES (:discription, :path, :title, :street, :postal, :city, :user_id, :number)",
                           discription=discription, path=path, title=title, street=street, postal=postal, city=city, user_id=session.get("user_id"), number=number)

                # Redirect to profile.html
                return redirect("/")

            # If image is not allowed redirect to upload.html
            else:
                return apology("File extensions is not allowed upload a JPEG, JPG, PNG or GIF file ")

        # If user didnt upload a picture
        else:
            return apology("Upload a picture of the studyspot")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("upload.html")


# Non route functions
def errorhandler(e):
    """ Handle error """
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


for code in default_exceptions:
    """ Listen for errors """
    app.errorhandler(code)(errorhandler)


def allowed_image(filename):
    """ Checks if image file has allowed extension """

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
    """ Checks if image is not too large """

    # Return true if image is not larger then set maximum
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False