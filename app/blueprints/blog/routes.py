from flask import render_template, url_for
from .import blog as app

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

@app.route("/blog")
def blog():
    return "this is the blog"

@app.route("/post/<int:id>")
def get_post(id):
    print(id)
    for p in posts:
        if p['id'] == id:
            post = p
            break
    context = {
        'p': post
    }
    return render_template("blog-post.html", **context)