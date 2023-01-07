import os
from dotenv import load_dotenv

load_dotenv()

#global constants
CURR_USER_KEY='curr_user'
UPLOAD_FOLDER="static/uploads"

ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif'}
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    # STATIC_FOLDER='static'
    # TEMPLATES_FOLDER='templates'
    SECRET_KEY= os.environ.get("SECRET_KEY")
    
    # DB
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    SQLALCHEMY_ECHO= True
    
    

    MAIL_SERVER= 'smtp.sendgrid.net'
    MAIL_PORT= 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD= os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    


class ProdConfig(Config):
    FLASK_ENV='production'
    DEBUG=False
    FLASK_DEBUG=False
    TESTING=False
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL','PROD_DATABASE_URI')
    

class DevConfig(Config):
    FLASK_ENV='development'
    DEBUG=True 
    FLASK_DEBUG=True #this doesn't work, have to set EXPORT DEBUG=True in terminal
    TESTING=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URI')
    DEBUG_TB_INTERCEPT_REDIRECTS= False
    UPLOAD_FOLDER=UPLOAD_FOLDER