from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import appEnvironment, DevConfig

appConfig = None
if appEnvironment == 'production':
    from config import ProdConfig
    appConfig = ProdConfig()
else:
    appConfig = DevConfig()

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(appConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .admin import admin_routes  # Import Admin routes
        from .main import main_routes # Import main application routes
        
        ma.init_app(app)
        db.create_all()  # Create database tables for our data models

        return app