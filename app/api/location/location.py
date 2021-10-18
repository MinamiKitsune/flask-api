from flask_restful import Resource
from . import location_api

# This class will handle all of the methods related to the location where a
# vacine will be administered
class Location(Resource):
    def get(self):
        return {"response" : "location"}, 200

# Add the resource to the API
location_api.add_resource(Location, '/')
