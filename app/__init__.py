from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Message, Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'authentication.login'
    login_manager.login_message = 'You do not have acces to this page. Please login to continue.'
    login_manager.login_message_category = 'danger'
    moment.init_app(app)
    mail.init_app(app)

    from app.blueprints.blog import blog
    app.register_blueprint(blog)
    
    from app.blueprints.authentication import authentication
    app.register_blueprint(authentication)

    with app.app_context():
        # building the rest of the flask application (configurations, additional packages, etc)
        from app.blueprints.shop import shop
        app.register_blueprint(shop)
        from app.blueprints.main import main
        app.register_blueprint(main)
        from .import context_processors
       

    return app