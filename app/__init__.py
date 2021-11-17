from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

db = None


def create_app():
    # Create the flask application
    app = Flask(__name__)

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///vaccine.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    global db
    db = SQLAlchemy(app)

    # Import all of the blueprints
    from .api import test_bp
    from .api.vaccine import vaccine_BP
    from .api.vaccination import vaccination_bp
    from .api.location import location_bp
    from .api.citizen import citizen_bp

    # Create the parent blueprint
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    # Register all of the blueprints to the parent
    api_bp.register_blueprint(test_bp)
    api_bp.register_blueprint(vaccine_BP)
    api_bp.register_blueprint(vaccination_bp)
    api_bp.register_blueprint(location_bp)
    api_bp.register_blueprint(citizen_bp)

    # Register the parent blueprint
    app.register_blueprint(api_bp)

    return app
