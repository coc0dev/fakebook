from flask import Blueprint

authentication = Blueprint('authentication', __name__, url_prefix="/authentication")

from .import routes, models