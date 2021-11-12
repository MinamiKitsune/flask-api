from flask_restful import Resource
from . import test_api

# This class is used to test the connection to the API
class TestConnection(Resource):
    def get(self):
        return {"response" : "successful"}, 200

# Add the resources to the API
test_api.add_resource(TestConnection, '/')
