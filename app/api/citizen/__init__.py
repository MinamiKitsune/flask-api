from flask import Blueprint
from flask_restful import Api

# Create the blueprints and the API
citizen_BP = Blueprint('citizen', __name__, url_prefix='/citizen')
dependant_BP = Blueprint('dependant', __name__, url_prefix='/dependant')
citizen_BP.register_blueprint(dependant_BP) # Register the blueprint to the parent blueprint
dependant_api = Api(dependant_BP)
citizen_api = Api(citizen_BP)

from . import citizen
from . import dependant