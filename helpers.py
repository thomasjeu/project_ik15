import requests
import urllib.parse
import os

from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session
from flask_session import Session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///admin.db")


def apology(message, code=400):
    """ Render message as an apology to user """

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


def change_description(description, user_id):
    """ Changes user description """

    # Update description in database
    db.execute("UPDATE users SET description=:description WHERE id=:user_id", user_id=user_id, description=description)

    return True


def change_password(password, confirmation, user_id):
    """ Changes password """

    # Hashes the password
    hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    # Update password in database
    db.execute("UPDATE users SET hash=:hash WHERE id=:user_id", user_id=user_id, hash=hash)

    return True


def change_username(username, user_id):
    """ Changes the username """

    # Update username in database
    db.execute("UPDATE users SET username=:username WHERE id=:user_id", user_id=user_id, username=username)

    return True


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


def fill_post_dict(posts):
    """ Fill post_dict with amount of likes the post has """

    post_dict = {}

    # Fills the post_dict with amount of likes, title and path
    for post in posts:
        likes = len(db.execute("SELECT post_id FROM likes WHERE post_id=:post_id", post_id=post["id"]))
        titles = db.execute("SELECT title FROM uploads WHERE id=:id", id=post["id"])
        title = titles[0]["title"]
        post_dict[post["id"]] = (post["path"], likes, title)

    return post_dict


def is_following(followers, user_id):
    """ False if user follows user already """

    for user in followers:
        if user["user_id"] == user_id:
            return False

    return True


def is_user(user, user_id):
    """ False if user looks at his own page """

    if user == user_id:
        return False

    return True


def liked_post(user_id, post_id):
    """ False if user already liked this post """

    liking = db.execute("SELECT post_id FROM likes WHERE user_id=:user_id AND post_id=:post_id",
                        user_id=session.get("user_id"), post_id=post_id)

    if liking:
        return False

    return True


def favo_post(user_id, post_id):
    """ False if user already favorited this post """

    favos = db.execute("SELECT post_id FROM favorites WHERE user_id=:user_id AND post_id=:post_id",
                       user_id=session.get("user_id"), post_id=post_id)

    if favos:
        return False

    return True


def user_information(user_id):
    """ Returns user information for profile page """

    # Get user info
    description = db.execute("SELECT description FROM users WHERE id=:user_id", user_id=user_id)[0]["description"]
    username = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=user_id)[0]["username"]
    posts = db.execute("SELECT path, id FROM uploads WHERE user_id=:user_id", user_id=user_id)
    picture = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=user_id)
    followers = db.execute("SELECT user_id FROM follow WHERE follow_id=:follow_id", follow_id=user_id)
    following = db.execute("SELECT follow_id FROM follow WHERE user_id=:user_id", user_id=user_id)

    # Return user info
    return description, username, posts, picture, followers, following


def user_information_users(user_id):
    """ Returns user information for profile page """

    # Get user info
    description = db.execute("SELECT description FROM users WHERE id=:user_id", user_id=user_id)[0]["description"]
    username = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=user_id)[0]["username"]
    posts = db.execute("SELECT path, id FROM uploads WHERE user_id=:user_id AND status=1", user_id=user_id)
    picture = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=user_id)
    followers = db.execute("SELECT user_id FROM follow WHERE follow_id=:follow_id", follow_id=user_id)
    following = db.execute("SELECT follow_id FROM follow WHERE user_id=:user_id", user_id=user_id)

    # Return user info
    return description, username, posts, picture, followers, following