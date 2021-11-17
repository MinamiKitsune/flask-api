from flask import Blueprint
from flask_restful import Api

# Create the blueprints and the API
citizen_bp = Blueprint('citizen', __name__, url_prefix='/citizen')
dependant_bp = Blueprint('dependant', __name__, url_prefix='/dependant')
citizen_bp.register_blueprint(dependant_bp)  # Register the blueprint to the parent blueprint
dependant_api = Api(dependant_bp)
citizen_api = Api(citizen_bp)

from . import citizen
from . import dependant
