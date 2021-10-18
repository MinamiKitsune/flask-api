from flask_restful import Resource
from . import dependant_api

class Dependant(Resource):
    def get(self):
        return {"response" : "dependant"}, 200

dependant_api.add_resource(Dependant, '/')