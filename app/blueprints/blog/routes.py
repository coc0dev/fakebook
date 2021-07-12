from flask import render_template, url_for, request, flash, redirect
from .import blog as app
from app.blueprints.blog.models import Post
from flask_login import current_user, login_required
from app import db

# posts = [
#         {
#             'id': 1,
#             'body': "This is the first blog post",
#             'author': "Somebody A. Someone",
#             'timestamp': "7-6-21"
#         },
#         {
#             'id': 2,
#             'body': "This is the second blog post",
#             'author': "Somebody B. Someone",
#             'timestamp': "7-5-21"
#         },
#         {
#             'id': 3,
#             'body': "This is the third blog post",
#             'author': "Somebody C. Someone",
#             'timestamp': "7-4-21"
#         }
#     ]

@app.route("/")
def index():
    context = {
        "posts": Post.query.all()
    }
    return render_template("index.html", **context)

@app.route("/blog")
def blog():
    pass

@app.route("/post/<int:id>")
@login_required
def get_post(id):
    context = {
        'p': Post.query.get(id)
    }
    return render_template("blog-post.html", **context)