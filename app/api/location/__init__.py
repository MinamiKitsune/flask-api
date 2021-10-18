from flask import Blueprint
from flask_restful import Api

location_BP = Blueprint('location', __name__, url_prefix='/location')
location_api = Api(location_BP)

from . import location