from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
from . import dependant_api
from ..database_models import Citizen
from ..decorator import token_required
from .. import data_handler, sms_handler
from app import db

# Parser to check that required arguments are sent to add dependant to the database
dependant_put_args = reqparse.RequestParser()
dependant_put_args.add_argument("id_citizen", type=str, required=True,
                                help="The ID of the citizen is required. The argument should be a String.")
dependant_put_args.add_argument("email", type=str, required=True,
                                help="The email of the citizen is required. The argument should be a String.")
dependant_put_args.add_argument("name", type=str, required=True,
                                help="The name of the citizen is required. The argument should be a String.")
dependant_put_args.add_argument("surname", type=str, required=True,
                                help="The surname of the citizen is required. The argument should be a String.")
dependant_put_args.add_argument("date_of_birth", type=str, required=True,
                                help="The date of birth of the citizen is required in the format YYYY-MM-DD. "
                                     "The argument should be a String.")
dependant_put_args.add_argument("mobile_num", type=str, required=True,
                                help="The mobile number of the citizen is required. The argument should be a String.")
dependant_put_args.add_argument("medical_aid", type=str,
                                help="The medical aid number of the citizen should be a String.")
dependant_put_args.add_argument("citizen_address", type=str,
                                help="The citizen address should be a String.")
dependant_put_args.add_argument("parent_id", type=str, required=True,
                                help="The ID of the parent is required. The argument should be a String.")

# Parser to check that required arguments are sent to get a dependant from the database
dependant_get_args = reqparse.RequestParser()
dependant_get_args.add_argument("parent_id", type=str, required=True,
                                help="The ID of the citizen is required. The argument should be a String.")

# Parser to check that required arguments are sent to update a dependant in the database
dependant_patch_args = reqparse.RequestParser()
dependant_patch_args.add_argument("id_citizen", type=str, required=True,
                                  help="The ID of the citizen is required. The argument should be a String.")
dependant_patch_args.add_argument("email", type=str,
                                  help="The citizen email address should be a String.")
dependant_patch_args.add_argument("name", type=str,
                                  help="The citizen name should be a String.")
dependant_patch_args.add_argument("surname", type=str,
                                  help="The citizen surname should be a String.")
dependant_patch_args.add_argument("date_of_birth", type=str,
                                  help="The date of birth of the citizen is should be in the format YYYY-MM-DD. "
                                       "The argument should be a String.")
dependant_patch_args.add_argument("mobile_num", type=str,
                                  help="The mobile number of the citizen should be a String")
dependant_patch_args.add_argument("medical_aid", type=str,
                                  help="The medical aid number of the citizen should be a String.")
dependant_patch_args.add_argument("citizen_address", type=str,
                                  help="Address is required in string format")
dependant_patch_args.add_argument("parent_id", type=str,
                                  help="The ID of the parent is required. The argument should be a String.")

# Parser to check that required arguments are sent to delete a citizen from the database
dependant_del_args = reqparse.RequestParser()
dependant_del_args.add_argument("id_citizen", type=str, required=True,
                                help="The ID of the citizen is required. The argument should be a String.")

# Fields to marshal the responses
resource_fields = {
    'id_citizen': fields.String,
    'email': fields.String,
    'name': fields.String,
    'surname': fields.String,
    'date_of_birth': fields.String,
    'mobile_num': fields.String,
    'medical_aid': fields.String,
    'citizen_address': fields.String,
    'parent_id': fields.String
}


# Class to handle methods related to dependants
class DependantResource(Resource):
    @marshal_with(resource_fields)
    @token_required
    def get(self):
        try:
            args = dependant_get_args.parse_args()
            data_handler.clean_data(args)
            return get_dependant(args), 200
        except Exception:
            abort(500, message="An internal server error has occurred, please try again later.")

    @token_required
    def put(self):
        try:
            args = dependant_put_args.parse_args()
            data_handler.clean_data(args)
            add_dependant(args)
            return {"message": "Added to database"}, 201
        except Exception:
            abort(500, message="An internal server error has occurred, please try again later.")

    @token_required
    def patch(self):
        try:
            args = dependant_patch_args.parse_args()
            data_handler.clean_data(args)
            update_dependant(args)
            return {"message": "Updated the database"}, 200
        except Exception:
            abort(500, message="An internal server error has occurred, please try again later.")

    @token_required
    def delete(self):
        try:
            if data_handler.check_if_admin(request.headers['x-access-token']):
                args = dependant_del_args.parse_args()
                data_handler.clean_data(args)
                delete_dependant(args)
                return {"message": "Deleted from database"}, 204
            else:
                abort(403, message="Forbidden.")
        except Exception:
            abort(500, message="An internal server error has occurred, please try again later.")


# Add resource to the API
dependant_api.add_resource(DependantResource, "")


# Get a dependant by their ID and return the full database entry
def get_dependant(args):
    result = Citizen.query.filter_by(parent_id=args["parent_id"]).all()
    if result:
        return result
    else:
        abort(404, message="A dependant with this parentID does not exist")


# Add a dependant to the database
def add_dependant(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if result:
        abort(409, message="A dependant with this ID already exists")
    else:
        result = Citizen.query.filter_by(id_citizen=args["parent_id"]).first()
        if result:
            try:
                date = datetime.strptime(args["date_of_birth"], '%Y-%m-%d')
                new_dependant = Citizen(id_citizen=args["id_citizen"], email=args["email"], name=args["name"],
                                        surname=args["surname"], date_of_birth=date,
                                        mobile_num=args["mobile_num"], medical_aid=args["medical_aid"],
                                        citizen_address=args["citizen_address"], parent_id=args["parent_id"])
                db.session.add(new_dependant)
                db.session.commit()
                sms_handler.send_mock_sms("A dependant has been added", result.mobile_num)
            except ValueError:
                abort(400, message="The date should be in format YYYY-MM-DD")
        else:
            abort(404, message="A parent with this ID does not exist")


# Update the dependant in the database
def update_dependant(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if not result:
        abort(404, message="A dependant with this ID does not exist, cannot update")
    else:
        if args["email"]:
            result.email = args["email"]
        if args["name"]:
            result.name = args["name"]
        if args["surname"]:
            result.surname = args["surname"]
        if args["date_of_birth"]:
            try:
                date = datetime.strptime(args["date_of_birth"], '%Y-%m-%d')
                result.date_of_birth = date
            except ValueError:
                abort(400, message="The date should be in format YYYY-MM-DD")
        if args["mobile_num"]:
            result.mobile_num = args["mobile_num"]
        if args["medical_aid"]:
            result.medical_aid = args["medical_aid"]
        if args["citizen_address"]:
            result.citizen_address = args["citizen_address"]
        if args["parent_id"]:
            result.parent_id = args["parent_id"]
        db.session.commit()


# Delete a dependant from the database
def delete_dependant(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if not result:
        abort(404, message="Dependant with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()
