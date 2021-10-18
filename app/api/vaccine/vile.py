from flask_restful import Resource
from . import vile_api

# This class will handle all of the methods related to the viles of a vaccine
class Vile(Resource):
    def get(self):
        return {"response" : "vile"}, 200

# Add the resource to the API
vile_api.add_resource(Vile, "/")
