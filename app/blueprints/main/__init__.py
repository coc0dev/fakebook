from flask import Blueprint


main = Blueprint('main', __name__, url_prefix='/contact')

from .import routes


