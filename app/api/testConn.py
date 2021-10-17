from flask import Blueprint
from flask_restful import Resource

# Create the blueprint
test_BP = Blueprint('test', __name__, url_prefix='/test')

# This class is used to test the connection to the API
class TestConnection(Resource):
    def get(self):
        return {"response" : "successful"}, 200