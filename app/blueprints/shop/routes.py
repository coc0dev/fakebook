from flask import render_template, url_for, redirect, flash, request, session, current_app, jsonify, json
from .import shop as app
from .models import Product, Cart
from flask_login import current_user
import stripe
from app import db



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
    from app.context_processors import build_cart
    display_cart = build_cart()['cart_dict']
    session['session_display_cart'] = display_cart
    context = {
        'cart': display_cart.values(),
    }
    if not current_user.is_authenticated:
        flash('You must login to view the cart', 'warning')
        return redirect(url_for('authentication.login'))
    return render_template("cart.html", **context)

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

@app.route('/checkout', methods=['POST'])
def checkout():
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    dc = session.get('session_display_cart')

    lst = []
    for product in dc.values():
        product_dict = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product['name'],
                        'images': [product['image']],
                    },
                    'unit_amount': int(float(product['price'])*100),
                },
                'quantity': product['quantity'],
            }
        lst.append(product_dict)
    try:
        # HANDLE PAYMENT
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=lst,
            mode='payment',
            success_url='http://localhost:5000/shop/cart',
            cancel_url='http://localhost:5000/shop/cart',
        )

        # Return all items from cart
        [db.session.delete(i) for i in Cart.query.filter_by(user_id=current_user.id).all()]
        db.session.commit()

        flash('Your order was processed successfully', 'primary')
        return jsonify({ 'session_id': checkout_session.id })
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route("/failure")
def shop_failure():
    return "this action failed"

@app.route("/success")
def shop_success():
    return "this action succeeded"