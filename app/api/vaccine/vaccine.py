from flask_restful import Resource
from . import vaccine_api

class Vaccine(Resource):
    def get(self):
        return {"response" : "vaccine"}, 200

vaccine_api.add_resource(Vaccine, '/')