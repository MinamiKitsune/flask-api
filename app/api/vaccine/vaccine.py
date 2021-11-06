from flask_restful import Resource
from . import vaccine_api
from ..databaseModels import Vaccine
from app import db

# This class will handle all of the methods related to the the vaccines
class VaccineResource(Resource):
    def get(self):
        new_vaccine = Vaccine(vaccine_name = "test", target_disease = "test", number_to_administer = 2, dosage_interval = 0)
        db.session.add(new_vaccine)
        db.session.commit()
        return {"response" : "added vaccine"}, 200

# Add the resource to the API
vaccine_api.add_resource(VaccineResource, '/')
