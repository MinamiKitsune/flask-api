from flask_restful import Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
from . import citizen_api
from ..database_models import Citizen
from .. import data_handler, sms_handler
from app import db

# Parser to check that required arguments are sent to add a citizen to the database
citizen_put_args = reqparse.RequestParser()
citizen_put_args.add_argument("id_citizen", type=str, required=True,
                              help="The ID of the citizen is required. The argument should be a String.")
citizen_put_args.add_argument("email", type=str, required=True,
                              help="The email of the citizen is required. The argument should be a String.")
citizen_put_args.add_argument("name", type=str, required=True,
                              help="The name of the citizen is required. The argument should be a String.")
citizen_put_args.add_argument("surname", type=str, required=True,
                              help="The surname of the citizen is required. The argument should be a String.")
citizen_put_args.add_argument("date_of_birth", type=str, required=True,
                              help="The date of birth of the citizen is required in the format YYYY-MM-DD. "
                                   "The argument should be a String.")
citizen_put_args.add_argument("mobile_num", type=str, required=True,
                              help="The mobile number of the citizen is required. The argument should be a String.")
citizen_put_args.add_argument("medical_aid", type=str,
                              help="The medical aid number of the citizen should be a String.")
citizen_put_args.add_argument("citizen_address", type=str,
                              help="The citizen address should be a String.")

# Parser to check that required arguments are sent to get a citizen from the database
citizen_get_args = reqparse.RequestParser()
citizen_get_args.add_argument("id_citizen", type=str, required=True,
                              help="The ID of the citizen is required. The argument should be a String.")

# Parser to check that required arguments are sent to update a citizen in the database
citizen_patch_args = reqparse.RequestParser()
citizen_patch_args.add_argument("id_citizen", type=str, required=True,
                                help="The ID of the citizen is required. The argument should be a String.")
citizen_patch_args.add_argument("email", type=str,
                                help="The citizen email address should be a String.")
citizen_patch_args.add_argument("name", type=str,
                                help="The citizen name should be a String.")
citizen_patch_args.add_argument("surname", type=str,
                                help="The citizen surname should be a String.")
citizen_patch_args.add_argument("date_of_birth", type=str,
                                help="The date of birth of the citizen is should be in the format YYYY-MM-DD. "
                                     "The argument should be a String.")
citizen_patch_args.add_argument("mobile_num", type=str,
                                help="The mobile number of the citizen should be a String")
citizen_patch_args.add_argument("medical_aid", type=str,
                                help="The medical aid number of the citizen should be a String.")
citizen_patch_args.add_argument("citizen_address", type=str,
                                help="Address is required in string format")

# Parser to check that required arguments are sent to delete a citizen from the database
citizen_del_args = reqparse.RequestParser()
citizen_del_args.add_argument("id_citizen", type=str, required=True,
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
    'citizen_address': fields.String
}


# Class to handle methods related to citizens
class CitizenResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = citizen_get_args.parse_args()
        data_handler.clean_data(args)
        return get_citizen(args), 200

    def put(self):
        args = citizen_put_args.parse_args()
        data_handler.clean_data(args)
        add_citizen(args)
        return {"message": "Added to database"}, 201

    def patch(self):
        args = citizen_patch_args.parse_args()
        data_handler.clean_data(args)
        update_citizen(args)
        return {"message": "Updated the database"}, 200

    def delete(self):
        args = citizen_del_args.parse_args()
        data_handler.clean_data(args)
        delete_citizen(args)
        return {"message": "Deleted from database"}, 204


# Add resource to the API
citizen_api.add_resource(CitizenResource, "")


# Get a citizen by their ID and return the full database entry
def get_citizen(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if result:
        return result
    else:
        abort(404, message="A citizen with this ID does not exist")


# Add a citizen to the database
def add_citizen(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if result:
        abort(409, message="A citizen with this ID already exists")
    else:
        try:
            date = datetime.strptime(args["date_of_birth"], '%Y-%m-%d')
            new_citizen = Citizen(id_citizen=args["id_citizen"], email=args["email"], name=args["name"],
                                  surname=args["surname"], date_of_birth=date, mobile_num=args["mobile_num"],
                                  medical_aid=args["medical_aid"],
                                  citizen_address=args["citizen_address"])
            db.session.add(new_citizen)
            db.session.commit()
            sms_handler.send_mock_sms("You have been added", args["mobile_num"])
        except ValueError:
            abort(400, message="The date should be in format YYYY-MM-DD")


# Update the citizen in the database
def update_citizen(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if not result:
        abort(404, message="Citizen with this ID does not exist, cannot update")
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
        db.session.commit()


# Delete a citizen from the database
def delete_citizen(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if not result:
        abort(404, message="Citizen with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()
