from flask import Blueprint
from flask_restful import Api

# Create the blueprints and the API
vaccine_bp = Blueprint('vaccine', __name__, url_prefix='/vaccine')
vial_bp = Blueprint('vial', __name__, url_prefix='/vial')
vaccine_bp.register_blueprint(vial_bp)  # Register the blueprint to the parent blueprint
vial_api = Api(vial_bp)
vaccine_api = Api(vaccine_bp)

from . import vaccine
from . import vial
