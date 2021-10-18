from flask_restful import Resource
from . import vaccination_api

# This class will handle all of the methods related to the vaccination event
# where a citizen will be vacinated
class Vaccination(Resource):
    def get(self):
        return {"response" : "vaccination"}, 200

# Add the resource to the API
vaccination_api.add_resource(Vaccination, "/")
