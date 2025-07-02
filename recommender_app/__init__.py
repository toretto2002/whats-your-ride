from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def create_app():
    print("Creating Flask app...")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/whats-your-ride'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("Initializing Flask app with DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)

    @app.route("/")
    def healthcheck():
        try:
            print("Checking DB connection...")
            db.session.execute(text("SELECT 1"))
            return "DB Connected!", 200
        except Exception as e:
            return f"DB Connection failed: {e}", 500

    return app
