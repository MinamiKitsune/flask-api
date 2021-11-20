from flask import request
from flask_restful import Resource, abort
from . import test_api
from .decorator import token_required
from . import data_handler


# This class is used to test the connection to the API
class TestConnection(Resource):
    def get(self):
        return {"response": "successful"}, 200


class TestAuthorisation(Resource):
    @token_required
    def get(self):
        return {"response": "successful"}, 200


class TestAdmin(Resource):
    @token_required
    def get(self):
        if data_handler.check_if_admin(request.headers['x-access-token']):
            return {"response": "successful"}, 200
        else:
            abort(403, message="Forbidden.")


# Add the resources to the API
test_api.add_resource(TestConnection, '/')
test_api.add_resource(TestAuthorisation, '/auth')
test_api.add_resource(TestAdmin, '/admin')
