from flask_restful import Resource
from . import citizen_api

# This class will handle all of the methods related to the citizen
class Citizen(Resource):
    def get(self):
        return {"response" : "citizen"}, 200

# Add the resource to the API
citizen_api.add_resource(Citizen, '/')