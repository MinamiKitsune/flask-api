from flask import Blueprint
from flask_restful import Api

test_BP = Blueprint('test', __name__, url_prefix='/test')
test_api = Api(test_BP)

from . import testConn