from flask_restful import Resource
from . import vial_api
from ..databaseModels import Vial
from .. import dataHandler
from app import db

# Parser to check if the required arguments are sent to get vile data
vial_get_args = reqparse.RequestParser()
vial_get_args.add_argument("id_vial", type=str, help="The ID of the vial in String format", required=True)

# Parser to check if the required arguments are sent to get vile data
vial_put_args = reqparse.RequestParser()
vial_put_args.add_argument("id_vial", type=str, help="The ID of the vial in String format", required=True)
vial_put_args.add_argument("id_vaccine", type=int, help="The ID of the vaccine in Int format", required=True)

# Parser to check if the required arguments are sent to get vile data
vial_patch_args = reqparse.RequestParser()
vial_patch_args.add_argument("id_vial", type=str, help="The ID of the vial in String format", required=True)
vial_patch_args.add_argument("id_vaccine", type=int, help="The ID of the vaccine in Int format", required=True)

# Parser to check if the required arguments are sent to get vile data
vial_patch_args = reqparse.RequestParser()
vial_patch_args.add_argument("id_vial", type=str, help="The ID of the vial in String format", required=True)

# fields to marshal the responses
resource_fields = {
    'id_vial' : fields.String,
    'id_vaccine': fields.Integer,
    'vaccine_name': fields.String,
    'target_disease': fields.String,
    'number_to_administer': fields.Integer,
    'dosage_interval': fields.Integer
}

# This class will handle all of the methods related to the vials of a vaccine
class VialResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = vial_get_args.parse_args()
        dataHandler.cleanData(args)
        getVile(args)
    
    def put(self):
        args = vial_put_args.parse_args()
        dataHandler.cleanData(args)
        addVile(args)
        return { "message": "Added to database" }, 201
    
    def patch(self):
        args = vial_patch_args.parse_args()
        dataHandler.cleanData(args)
        updateVile(args)
        return { "message": "Updated the database" }, 200
    
    def delete(self):
        args = vaccine_patch_args.parse_args()
        deleteVile(args)
        return { "message": "Deleted from database" }, 204

# Add the resource to the API
vial_api.add_resource(VialResource, "")

# Get the vile from the database
def getVile(args):
    # TODO finish this
    return True

# Add the vile to the database
def addVile(args):
    # TODO finish this
    return True

# Update a vile in the database
def updateVile(args):
    # TODO finish this
    return True

# Delete a vile from the database
def deleteVile(args):
    # TODO finish this
    return True