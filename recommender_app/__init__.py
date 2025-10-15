from flask import Flask
from sqlalchemy import text
from recommender_app.extensions import db, migrate, jwt, cors
from . import models
from recommender_app.core.config import Config
from recommender_app.api.routes import blueprints
from recommender_app.core.logging_config import configure_logging



def create_app():
    app = Flask(__name__)

    configure_logging()

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
    
    # Initialize CORS with configuration
    cors.init_app(app, 
                  origins=app.config['CORS_ORIGINS'],
                  methods=app.config['CORS_METHODS'],
                  allow_headers=app.config['CORS_ALLOW_HEADERS'],
                  supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])

    print("Extensions initialized.")


def configure_blueprints(app):
    for bp in blueprints:
        app.register_blueprint(bp)
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
