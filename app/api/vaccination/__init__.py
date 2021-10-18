from flask import Blueprint
from flask_restful import Api

# Create the blueprints and the API
vaccination_BP = Blueprint('vaccination', __name__, url_prefix='/vaccination')
vaccination_api = Api(vaccination_BP)

from . import vaccination
