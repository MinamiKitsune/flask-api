from flask_restful import Resource
from . import dependant_api

# This class will contain all the methods related to a dependant
class Dependant(Resource):
    def get(self):
        return {"response" : "dependant"}, 200

# Add the resource to the API
dependant_api.add_resource(Dependant, '/')