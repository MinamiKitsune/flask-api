from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
db = None

def create_app():
    # Create the flask application
    app = Flask(__name__)

    # Database
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///vaccine.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    global db
    db = SQLAlchemy(app)

    # Import all of the blueprints
    from .api import test_BP
    from .api.vaccine import vaccine_BP
    from .api.vaccination import vaccination_BP
    from .api.location import location_BP
    from .api.citizen import citizen_BP

    # Create the parent blueprint
    api_BP = Blueprint('api', __name__, url_prefix='/api')

    # Register all of the blueprints to the parent
    api_BP.register_blueprint(test_BP)
    api_BP.register_blueprint(vaccine_BP)
    api_BP.register_blueprint(vaccination_BP)
    api_BP.register_blueprint(location_BP)
    api_BP.register_blueprint(citizen_BP)

    # Register the parent blueprint
    app.register_blueprint(api_BP)

    return app