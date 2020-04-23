from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath( path.dirname( __file__ ) )
load_dotenv( path.join( basedir, ".env" ) )


class Config:
    """Set Flask configuration variables from the .env file """

    # General Flask Config
    SECRET_KEY = environ.get( "SECRET_KEY" )
    FLASK_ENV = environ.get( "FLASK_ENV" )
    FLASK_APP = environ.get( "FLASK_APP" )
    #FLASK_DEBUG = 1


class ProdConfig(Config):
    DEBUG = environ.get("DEBUG")
    TESTING = environ.get("TESTING")
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATONS = Config.FLASK_ENV


class DevConfig(Config):
    DEBUG = environ.get("DEBUG")
    TESTING = environ.get("TESTING")
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATONS = Config.FLASK_ENV