from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevConfig

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .admin import admin_routes  # Import Admin routes
        from .main import main_routes # Import main application routes
        
        db.create_all()  # Create database tables for our data models

        return app