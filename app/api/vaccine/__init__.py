from flask import Blueprint
from flask_restful import Api

# Create the blueprints and the API
vaccine_BP = Blueprint('vaccine', __name__, url_prefix='/vaccine')
vial_BP = Blueprint('vial', __name__, url_prefix='/vial')
vaccine_BP.register_blueprint(vile_BP) # Register the blueprint to the parent blueprint
vial_api = Api(vial_BP)
vaccine_api = Api(vaccine_BP)

from . import vaccine
from . import vial
