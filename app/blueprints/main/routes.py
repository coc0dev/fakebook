from flask import render_template, url_for
from .import main as app

posts = [
        {
            'id': 1,
            'body': "This is the first blog post",
            'author': "Somebody A. Someone",
            'timestamp': "7-6-21"
        },
        {
            'id': 2,
            'body': "This is the second blog post",
            'author': "Somebody B. Someone",
            'timestamp': "7-5-21"
        },
        {
            'id': 3,
            'body': "This is the third blog post",
            'author': "Somebody C. Someone",
            'timestamp': "7-4-21"
        }
    ]

@app.route("/")
def index():
    context = {
        "posts": posts
    }
    return render_template("index.html", **context)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/profile")
def profile():
    logged_in_user = "Evan"
    return render_template('profile.html', u=logged_in_user)