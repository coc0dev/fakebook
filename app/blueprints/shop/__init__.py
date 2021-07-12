from flask import Blueprint

shop = Blueprint('shop', __name__, url_prefix="/shop")

from .import routes, models
