from flask_restful import Resource
from . import vial_api
from ..databaseModels import Vial
from app import db

# This class will handle all of the methods related to the vials of a vaccine
class VialResource(Resource):
    def get(self):
        new_vial = Vial(id_vial = "11111", vaccine_id = 1)
        db.session.add(new_vial)
        db.session.commit()
        return {"response" : "Vial added"}, 200

# Add the resource to the API
vial_api.add_resource(VialResource, "/")
