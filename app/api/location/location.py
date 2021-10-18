from flask_restful import Resource
from . import location_api

class Location(Resource):
    def get(self):
        return {"response" : "location"}, 200

location_api.add_resource(Location, '/')