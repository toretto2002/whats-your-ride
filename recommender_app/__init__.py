from flask import Flask
from sqlalchemy import text
from .extensions import db, migrate, jwt
from . import models
from recommender_app.routes.user_routes import bp as user_routes
from recommender_app.core.config import Config


def create_app():
    app = Flask(__name__)

    # Load configuration
    configure_app(app)

    # Initialize extensions
    configure_extensions(app)

    # Register blueprints
    configure_blueprints(app)

    # Healthcheck route
    add_healthcheck_route(app)

    return app


def configure_app(app):
    app.config.from_object(Config)

    print("Flask configuration loaded.")


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize JWT
    jwt.init_app(app)

    print("Extensions initialized.")


def configure_blueprints(app):
    app.register_blueprint(user_routes)
    print("Blueprints registered.")


def add_healthcheck_route(app):
    @app.route("/")
    def healthcheck():
        try:
            print("Checking DB connection...")
            db.session.execute(text("SELECT 1"))
            return "DB Connected!", 200
        except Exception as e:
            return f"DB Connection failed: {e}", 500
