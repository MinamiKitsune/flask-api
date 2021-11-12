from flask_restful import Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
from . import citizen_api
from ..databaseModels import Citizen
from .. import dataHandler, smsHandler
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
help="The date of birth of the citizen is required in the format YYYY-MM-DD. The argument should be a String.")
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
help="The date of birth of the citizen is should be in the format YYYY-MM-DD. The argument should be a String.")
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
        try:
            args = citizen_get_args.parse_args()
            dataHandler.cleanData(args)
            return getCitizen(args), 200
        except Exception:
            abort(500, message="An internal server error has occured, please try again later.")

    def put(self):
        try:
            args = citizen_put_args.parse_args()
            dataHandler.cleanData(args)
            addCitizen(args)
            return { "message": "Added to database" }, 201
        except Exception:
            abort(500, message="An internal server error has occured, please try again later.")
    
    def patch(self):
        try:
            args = citizen_patch_args.parse_args()
            dataHandler.cleanData(args)
            updateCitizen(args)
            return { "message": "Updated the database" }, 200
        except Exception:
            abort(500, message="An internal server error has occured, please try again later.")
    
    def delete(self):
        try:
            args = citizen_del_args.parse_args()
            dataHandler.cleanData(args)
            deleteCitizen(args)
            return { "message": "Deleted from database" }, 204
        except Exception:
            abort(500, message="An internal server error has occured, please try again later.")

# Add resource to the API
citizen_api.add_resource(CitizenResource, "")

# Get a citizen by their ID and return the full database entry
def getCitizen(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if result:
        return result
    else:
        abort(404, message="A citizen with this ID does not exist")

# Add a citizen to the database
def addCitizen(args):
    result = Citizen.query.filter_by(id_citizen = args["id_citizen"]).first()
    if result:
        abort(409, message="A citizen with this ID already exists")
    else:
        try:
            date = datetime.strptime(args["date_of_birth"], '%Y-%m-%d')
        except ValueError:
            abort(400, message="The date should be in format YYYY-MM-DD")
        new_citizen = Citizen(id_citizen = args["id_citizen"], email = args["email"], name = args["name"],
        surname = args["surname"], date_of_birth = date, mobile_num = args["mobile_num"], medical_aid = args["medical_aid"],
        citizen_address = args["citizen_address"])
        db.session.add(new_citizen)
        db.session.commit()
        smsHandler.sendMockSms("You have been added", args["mobile_num"])

# Update the citizen in the database
def updateCitizen(args):
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
            except ValueError:
                abort(400, message="The date should be in format YYYY-MM-DD")
            result.date_of_birth = date
        if args["mobile_num"]:
            result.mobile_num = args["mobile_num"]
        if args["medical_aid"]:
            result.medical_aid = args["medical_aid"]
        if args["citizen_address"]:
            result.citizen_address = args["citizen_address"]
        db.session.commit()

# Delete a citizen from the database
def deleteCitizen(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if not result:
        abort(404, message="Citizen with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()
