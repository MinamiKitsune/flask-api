from flask import Blueprint
from flask_restful import Api

# Create the blueprint and the API
test_bp = Blueprint('test', __name__, url_prefix='/test')
test_api = Api(test_bp)

from . import test_conn
