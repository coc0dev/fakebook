from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.blueprints.blog import blog
    app.register_blueprint(blog)
    from app.blueprints.shop import shop
    app.register_blueprint(shop)
    from app.blueprints.main import main
    app.register_blueprint(main)

    with app.app_context():

# building the rest of the flask application (configurations, additional packages, etc)
        from  .import routes

    return app