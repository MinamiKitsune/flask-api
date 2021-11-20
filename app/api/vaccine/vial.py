from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import vial_api
from ..database_models import Vial, Vaccine
from .. import data_handler
from app import db

# Parser to check if the required arguments are sent to get vial data from the database
vial_get_args = reqparse.RequestParser()
vial_get_args.add_argument("id_vial", type=str, required=True,
                           help="The ID of the vial in String format is required")

# Parser to check if the required arguments are sent to add vial data to the database
vial_put_args = reqparse.RequestParser()
vial_put_args.add_argument("id_vial", type=str, required=True,
                           help="The ID of the vial in String format is required")
vial_put_args.add_argument("vaccine_id", type=int, required=True,
                           help="The ID of the vaccine in Int format is required")

# Parser to check if the required arguments are sent to update vial data in the database
vial_patch_args = reqparse.RequestParser()
vial_patch_args.add_argument("id_vial", type=str, required=True,
                             help="The ID of the vial in String format is required")
vial_patch_args.add_argument("vaccine_id", type=int, required=True,
                             help="The ID of the vaccine in Int format is required")

# Parser to check if the required arguments are sent to delete vial data from the database
vial_del_args = reqparse.RequestParser()
vial_del_args.add_argument("id_vial", type=str, required=True,
                           help="The ID of the vial in String format is required")

# fields to marshal the responses
resource_fields = {
    'id_vial': fields.String,
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
        data_handler.remove_space(args)
        return get_vial(args), 200

    def put(self):
        args = vial_put_args.parse_args()
        data_handler.remove_space(args)
        add_vial(args)
        return {"message": "Added to database"}, 201

    def patch(self):
        args = vial_patch_args.parse_args()
        data_handler.remove_space(args)
        update_vial(args)
        return {"message": "Updated the database"}, 200

    def delete(self):
        args = vial_del_args.parse_args()
        data_handler.remove_space(args)
        delete_vial(args)
        return {"message": "Deleted from database"}, 204


# Add the resource to the API
vial_api.add_resource(VialResource, "")


# Get the vial from the database
def get_vial(args):
    result = db.session.query(
        Vial.id_vial, Vial.vaccine_id,
        Vaccine.vaccine_name, Vaccine.target_disease, Vaccine.number_to_administer, Vaccine.dosage_interval
    ).filter_by(id_vial=args["id_vial"]).join(Vaccine).first()
    if result:
        return result
    else:
        abort(404, message="Vial with this ID does not exist")
    return True


# Add the vial to the database
def add_vial(args):
    if vaccine_exists(args):
        result = Vial.query.filter_by(id_vial=args["id_vial"]).first()
        if result:
            abort(409, message="This vial has already been added to the database")
        else:
            new_vial = Vial(id_vial=args["id_vial"], vaccine_id=args["vaccine_id"])
            db.session.add(new_vial)
            db.session.commit()


# Update a vial in the database
def update_vial(args):
    result = Vial.query.filter_by(id_vial=args["id_vial"]).first()
    if not result:
        abort(404, message="Vial with this ID does not exist, cannot update")
    else:
        if vaccine_exists(args):
            result.vaccine_id = args["vaccine_id"]
            db.session.commit()


# Delete a vial from the database
def delete_vial(args):
    result = Vial.query.filter_by(id_vial=args["id_vial"]).first()
    if not result:
        abort(404, message="A vial with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()


# Checks if the vaccine exists
def vaccine_exists(args):
    if Vaccine.query.filter_by(id_vaccine=args["vaccine_id"]).first():
        return True
    else:
        abort(404,
              message="Vaccine with this ID does not exist, please query the vaccines to find the correct vaccine ID")
