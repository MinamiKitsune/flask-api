from flask_restful import Resource
from . import vaccination_api

class Vaccination(Resource):
    def get(self):
        return {"response" : "vaccination"}, 200

vaccination_api.add_resource(Vaccination, "/")