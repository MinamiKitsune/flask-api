from flask_restful import Resource
from . import vile_api

class Vile(Resource):
    def get(self):
        return {"response" : "vile"}, 200

vile_api.add_resource(Vile, "/")