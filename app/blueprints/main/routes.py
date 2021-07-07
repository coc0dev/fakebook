from flask import render_template, url_for
from .import main as app

@app.route("/contact")
def contact():
    return render_template("contact.html")