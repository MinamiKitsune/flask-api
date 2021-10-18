from flask_restful import Resource
from . import vaccine_api

# This class will handle all of the methods related to the the vaccines
class Vaccine(Resource):
    def get(self):
        return {"response" : "vaccine"}, 200

# Add the resource to the API
vaccine_api.add_resource(Vaccine, '/')
