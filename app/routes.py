from app import app
from flask import jsonify, render_template

"""
CREATE - POST
READ - GET
UPDATE - PUT
DELETE - DELETE
"""

@app.route("/")
def index():
    return "hello world!"

@app.route("/profile")
def profile():
    logged_in_user = "Evan"
    return render_template('profile.html', u=logged_in_user)

@app.route("/blog")
def blog():
    return "this is the blog"

@app.route("/contact")
def contact():
    return "this is the contact"