from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import vial_api
from ..databaseModels import Vial, Vaccine
from .. import dataHandler
from app import db


# Parser to check if the required arguments are sent to get vial data
vial_get_args = reqparse.RequestParser()
vial_get_args.add_argument("id_vial", type=str, help="The ID of the vial in String format", required=True)

# Parser to check if the required arguments are sent to get vial data
vial_put_args = reqparse.RequestParser()
vial_put_args.add_argument("id_vial", type=str, help="The ID of the vial in String format", required=True)
vial_put_args.add_argument("vaccine_id", type=int, help="The ID of the vaccine in Int format", required=True)

# Parser to check if the required arguments are sent to get vial data
vial_patch_args = reqparse.RequestParser()
vial_patch_args.add_argument("id_vial", type=str, help="The ID of the vial in String format", required=True)
vial_patch_args.add_argument("vaccine_id", type=int, help="The ID of the vaccine in Int format", required=True)

# Parser to check if the required arguments are sent to get vial data
vial_del_args = reqparse.RequestParser()
vial_del_args.add_argument("id_vial", type=str, help="The ID of the vial in String format", required=True)

# fields to marshal the responses
resource_fields = {
    'id_vial' : fields.String,
    'vaccine_id': fields.Integer,
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
        dataHandler.removeSpace(args)
        return getVial(args), 200
    
    def put(self):
        args = vial_put_args.parse_args()
        dataHandler.removeSpace(args)
        addVial(args)
        return { "message": "Added to database" }, 201
    
    def patch(self):
        args = vial_patch_args.parse_args()
        dataHandler.removeSpace(args)
        updateVial(args)
        return { "message": "Updated the database" }, 200
    
    def delete(self):
        args = vial_del_args.parse_args()
        deleteVial(args)
        return { "message": "Deleted from database" }, 204

# Add the resource to the API
vial_api.add_resource(VialResource, "")

# Get the vial from the database
def getVial(args):
    result = db.session.query(
    Vial.id_vial, Vial.vaccine_id,
    Vaccine.vaccine_name, Vaccine.target_disease, Vaccine.number_to_administer, Vaccine.dosage_interval
    ).filter_by(id_vial = args["id_vial"]).join(Vaccine).first()
    if result:
        return result
    else:
        abort(404, message="Vial with this ID does not exist")
    return True

# Add the vial to the database
def addVial(args):
    if vaccineExists(args):
        result = Vial.query.filter_by(id_vial=args["id_vial"]).first()
        if result:
            abort(409, message="This vial has already been added to the database")
        else:
            new_vial = Vial(id_vial = args["id_vial"], vaccine_id = args["vaccine_id"])
            db.session.add(new_vial)
            db.session.commit()

# Update a vial in the database
def updateVial(args):
    result = Vial.query.filter_by(id_vial=args["id_vial"]).first()
    if not result:
        abort(404, message="Vial with this ID does not exist, cannot update")
    else:
        if vaccineExists(args):
            result.vaccine_id = args["vaccine_id"]
            db.session.commit()

# Delete a vial from the database
def deleteVial(args):
    result = Vial.query.filter_by(id_vial=args["id_vial"]).first()
    if not result:
        abort(404, message="A vial with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()

# Checks if the vaccine exists
def vaccineExists(args):
    if Vaccine.query.filter_by(id_vaccine=args["vaccine_id"]).first():
        return True
    else:
        abort(404, message="Vaccine with this ID does not exist, please query the vaccines to find the correct vaccine ID")
