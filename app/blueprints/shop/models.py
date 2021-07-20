from app import db
from datetime import datetime
from app.blueprints.authentication.models import User

# class StripeProduct(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     stripe_product_id = db.Column(db.String)
#     name = db.Column(db.String)
#     image = db.Column(db.String)
#     description = db.Column(db.Text)
#     price = db.Column(db.Float)
#     tax = db.Column(db.Float)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def save(self):    
#         db.session.add(self)
#         db.session.commit()

#     def __repr__(self):
#         return f'<Product: {self.name} @{self.price}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    tax = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):    
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Product: {self.name} @{self.price}>'

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.ForeignKey('product.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        data = {
            'product': Product.query.get(self.product_id),
            'user': User.query.get(self.user_id)
        }
        return data

    def save(self):    
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Product: {self.user_id} | {self.product_id}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.ForeignKey('product.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):    
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Product: {self.user_id} | {self.product_id}>'
    
    