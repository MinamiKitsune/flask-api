from flask import Flask, Blueprint
from flask_restful import Api, url_for


# Import all of the blueprints
from .api.testConn import test_BP

# Import all of the classes
from .api.testConn import TestConnection


def create_app():
    # Create the flask application
    app = Flask(__name__)

    # Create the parent blueprint
    api_BP = Blueprint('api', __name__, url_prefix='/api')

    # Create the API
    api = Api(api_BP)

    # Register all of the blueprints to the parent
    api_BP.register_blueprint(test_BP)

    # Add all the resources to the API
    api.add_resource(TestConnection,'/test')

    # Register the parent blueprint
    app.register_blueprint(api_BP)

    return app