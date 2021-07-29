from .import api
from flask import jsonify, current_app, request
from app.blueprints.blog.models import Post
from flask_login import current_user
import stripe
import ast
import json

@api.route('/blog')
def get_posts():
    # posts = Post.query.all()
    return jsonify([p.to_dict() for p in Post.query.all()])

@api.route('/blog/user')
def get_user_posts():
    return jsonify([p.to_dict() for p in current_user.posts.all()])

@api.route('/shop/products')
def get_products():
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    return jsonify(stripe.Product.list())

@api.route('/shop/checkout', methods=["POST"])
def get_cart():
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    products = json.loads(request.get_data().decode('utf-8'))
    print(type(products))
    lst = []
    for product in products['items'].values():
        product_dict = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product['name'],
                        'images': product['images'],
                    },
                    'unit_amount': int(float(product["price"])),
                },
                'quantity': product['quantity'],
            }
        lst.append(product_dict)
    try:
        # HANDLE PAYMENT
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            # line_items=[{"price": "price_1JGQJNLH2Ct9I2iGZpU2j5rN", "quantity": 1}],
            line_items=lst,
            mode='payment',
            success_url='http://localhost:5000/shop/cart',
            cancel_url='http://localhost:5000/shop/cart',
        )

        # Return all items from cart
        # [db.session.delete(i) for i in Cart.query.filter_by(user_id=current_user.id).all()]
        # db.session.commit()
        # return jsonify(stripe.Cart.list_())
        return jsonify({ 'session_id': checkout_session.id })
        # redirect(url_for('shop.checkout'))
    except Exception as e:
        return jsonify(error=str(e)), 403