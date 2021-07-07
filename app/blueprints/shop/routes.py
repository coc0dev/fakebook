from flask import render_template, url_for
from .import shop as app

@app.route("/shop/products")
def shop_products():
    return render_template("products.html")

@app.route("/shop/cart")
def shop_cart():
    return render_template("cart.html")

@app.route("/shop/failure")
def shop_failure():
    return "this action failed"

@app.route("/shop/success")
def shop_success():
    return "this action succeeded"