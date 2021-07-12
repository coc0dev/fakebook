from flask import render_template, url_for, redirect, flash, request
from .import shop as app
from .models import Product, Cart
from flask_login import current_user

@app.route("/products")
def shop_products():
    """
    [GET] /shop/products
    """
    context = {
        'products': Product.query.all()
    }
    return render_template("products.html", **context)

@app.route("/cart")
def shop_cart():
    """
    [GET] /shop/cart
    """
    return render_template("cart.html")

@app.route('/cart/add')
def add_to_cart():
    """
    [GET] /shop/cart/add
    """ 
    if not current_user.is_authenticated:
        flash('You must login to add items to your cart', 'warning')
        return redirect(url_for('authencation.login'))
    # Make a new product
    product = Product.query.get(request.args.get('id'))
    # Save it to their cart
    Cart(user_id=current_user.id, product_id=product.id).save()
    flash(f'You added {product.name} to your cart', 'success')
    return redirect(url_for('shop.shop_products'))


@app.route("/failure")
def shop_failure():
    return "this action failed"

@app.route("/success")
def shop_success():
    return "this action succeeded"