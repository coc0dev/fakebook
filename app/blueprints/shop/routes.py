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
    # stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    # print(stripe.Product.list())
    # print(stripe.Price.retrieve("price_1JCnc72eZvKYlo2CyNkggxT1",))
    context = {
        'products': Product.query.all()
    }
    # print(StripeProduct.query.all())
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

@app.route('/update', methods=['POST'])
def update_cart():

    if request.method == 'POST':
        product = session["session_display_cart"].keys()
        for i, p in enumerate(product):
            new_item = int(request.form.get(f'quantity-{ p }'))
            cart = Cart.query.filter_by(user_id=current_user.id, product_id=p)

            while cart.count() != new_item:
                if cart.count() > new_item:
                    db.session.delete(cart.first())
                elif cart.count() < new_item:
                    Cart(user_id=current_user.id, product_id=p).save()

        db.session.commit()

        
        
        
    flash(f'You updated your cart.', 'success')
    return redirect(url_for('shop.shop_cart'))

@app.route('/delete', methods=['POST'])
def remove_from_cart():

    id = request.json['p']
    print(id)
    
    if request.method == 'POST':
        product = Product.query.get(id)
        print(product)
        remove = Cart.query.filter_by(user_id=current_user.id, product_id=product.id)
        print(remove)
        for r in remove:
            db.session.delete(remove.first())
            db.session.commit()
   
    
        flash(f'You updated your cart.', 'success')
    return redirect(url_for('shop.shop_cart'))

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
        redirect(url_for('shop.checkout'))
        return jsonify({ 'session_id': checkout_session.id })
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route("/failure")
def shop_failure():
    return "this action failed"

@app.route("/success")
def shop_success():
    return "this action succeeded"

# @app.route('/seed')
# def seed_stripe_products():
#     stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

#     def seed_data():
#         # print(stripe.Product.list().get('data'))
#         list_to_store_in_db = []

#         for p in stripe.Product.list().get('data'):
#             list_to_store_in_db.append(StripeProduct(stripe_product_id=p['id'], name=p['name'], image=p['images'][0], description=p['description'], price=int(float(p['metadata']['price']) * 100), tax=int(float(p['metadata']['tax']) * 100)))
        
#         db.session.add_all(list_to_store_in_db)
#         db.session.commit()

#     seed_data()
#     return jsonify({ 'message': 'Success' })

