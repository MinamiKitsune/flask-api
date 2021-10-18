from flask_restful import Resource
from . import citizen_api

class Citizen(Resource):
    def get(self):
        return {"response" : "citizen"}, 200

citizen_api.add_resource(Citizen, '/')