from flask import Blueprint
from flask_restful import Api

# Create the blueprints and the API
location_bp = Blueprint('location', __name__, url_prefix='/location')
location_api = Api(location_bp)

from . import location
