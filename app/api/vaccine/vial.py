from flask_restful import Resource
from . import vial_api

# This class will handle all of the methods related to the vials of a vaccine
class Vial(Resource):
    def get(self):
        return {"response" : "vial"}, 200

# Add the resource to the API
vial_api.add_resource(Vial, "/")
