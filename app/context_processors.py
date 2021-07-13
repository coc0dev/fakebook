from flask_login import current_user
from flask import current_app as app
from app.blueprints.shop.models import Cart, Product
from functools import reduce

@app.context_processor
def build_cart():
    cart_dict = {}
    if current_user.is_anonymous:
        return {
            'cart_dict': cart_dict,
            'cart_size': 0,
            'cart_subtotal': 0,
            'cart_tax': 0,
            'cart_grandtotal': 0,
        }
    # Find the User's Cart
    cart = Cart.query.filter_by(user_id=current_user.id).all()
    if len(cart) > 0:
        # Loop through the cart
        for cart_item in cart:
            # get the product info to store in the dictionary later
            product = Product.query.get(cart_item.product_id)
            if str(cart_item.product_id) not in cart_dict:
                cart_dict[str(product.id)] = {
                    'id': cart_item.product_id,
                    'product_id': product.id,
                    'image': product.image,
                    'quantity': 1,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'tax': product.tax
                }
            else:
                cart_dict[str(product.id)]['quantity']+=1
    
    def format_currency(price):
        return f'${price:,.2f}'
    
    return {
            'cart_dict': cart_dict,
            'cart_size': len(cart),
            'cart_subtotal': format_currency(reduce(lambda x,y:x+y, [i.to_dict()['product'].price for i in cart])) if cart else 0,
            'cart_tax': format_currency(reduce(lambda x,y:x+y, [i.to_dict()['product'].tax for i in cart])) if cart else 0,
            'cart_grandtotal': format_currency(reduce(lambda x,y:x+y, [i.to_dict()['product'].price + i.to_dict()['product'].tax for i in cart])) if cart else 0,
    }

@app.context_processor
def get_stripe_keys():
    return {
        'STRIPE_PUBLISHABLE_KEY': app.config.get('STRIPE_PUBLISHABLE_KEY')
    }