import os
from dotenv import load_dotenv

basedir = os.path.dirname(__name__)
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    FLASK_APP=os.getenv('FLASK_APP')
    FLASK_ENV=os.getenv('FLASK_ENV')
    
    if os.getenv('SQLALCHEMY_DATABASE_URI').startswith('postgres'):
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI').replace('postgres', 'postgresql')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    # aws_access_key_id = YOUR_KEY
    # aws_secret_access_key = YOUR_SECRET
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=os.getenv('MAIL_PORT')
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL')
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')