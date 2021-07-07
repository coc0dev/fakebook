from flask import render_template, url_for
from .import shop as app

@app.route("/products")
def shop_products():
    return render_template("products.html")

@app.route("/cart")
def shop_cart():
    return render_template("cart.html")

@app.route("/failure")
def shop_failure():
    return "this action failed"

@app.route("/success")
def shop_success():
    return "this action succeeded"