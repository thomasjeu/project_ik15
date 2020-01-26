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


def change_discription(discription, user_id):
    """Changes user discription"""

    # Update discription in database
    db.execute("UPDATE users SET discription=:discription WHERE id=:user_id", user_id=user_id, discription=discription)

    return True


def change_password(password, confirmation, user_id):
    """ Changes password """

    # Hashes the password
    hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    # Update password in database
    db.execute("UPDATE users SET hash=:hash WHERE id=:user_id", user_id=user_id, hash=hash)

    return True

def change_username(username, user_id):
    """Changes the username"""

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


def followers_following(id_dict, f_list, user_list):
    """Fills id_dict and a list with usernames"""
    for user in user_list:
        user = user["user_id"]
        username = db.execute("SELECT username FROM users WHERE id=:id", id=user)[0]["username"]
        f_list.append(username)
        id_dict[username] = user
    return id_dict, f_list


def fill_post_dict(posts):
    """Fill post_dict with amount of likes the post has"""
    post_dict = {}
    for post in posts:
            likes = db.execute("SELECT id FROM likes WHERE id=:id", id=post["id"])
            post_dict[post["id"]] = (post["path"], len(likes))
    return post_dict


def is_following(following):
    """True if user follows user already"""
    if following:
        return True
    return False


def is_user(user, user_id):
    """True if user looks at his own page"""
    if user == user_id:
        return True
    return False


def user_information(user_id):
    """Returns user information for profile page"""

    # Get user info
    discription = db.execute("SELECT discription FROM users WHERE id=:user_id", user_id=user_id)[0]["discription"]
    username = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=user_id)[0]["username"]
    posts = db.execute("SELECT path, id FROM uploads WHERE user_id=:user_id", user_id=user_id)
    picture = db.execute("SELECT image FROM users WHERE id=:user_id", user_id=user_id)
    followers = db.execute("SELECT user_id FROM follow WHERE follow_id=:follow_id", follow_id=user_id)
    following = db.execute("SELECT follow_id FROM follow WHERE user_id=:user_id", user_id=user_id)

    # Return user info
    return discription, username, posts, picture, followers, following