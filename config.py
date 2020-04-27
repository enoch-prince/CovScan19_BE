from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath( path.dirname( __file__ ) )
load_dotenv( path.join( basedir, ".env" ) )

appEnvironment = environ.get( "FLASK_ENV" )

# For mysql databse config
mysql_username = environ.get( "MYSQL_USERNAME" )
mysql_password = environ.get( "MYSQL_PASSWORD" )
mysql_db_name = environ.get( "MYSQL_DB_NAME" )
client_host = environ.get( "CLIENT_HOST" )

class Config:
    """Set Flask configuration variables from the .env file """

    # General Flask Config
    SECRET_KEY = environ.get( "SECRET_KEY" )
    FLASK_ENV = appEnvironment
    FLASK_APP = environ.get( "FLASK_APP" )


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"mysql://{mysql_username}:{mysql_password}@{client_host}/{mysql_db_name}"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATONS = Config.FLASK_ENV


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI') # for sqlite
    SQLALCHEMY_DATABASE_URI = f"mysql://{mysql_username}:{mysql_password}@{client_host}/{mysql_db_name}"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATONS = Config.FLASK_ENV