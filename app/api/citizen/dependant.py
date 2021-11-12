from flask_restful import Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
from . import dependant_api
from ..databaseModels import Citizen
from .. import dataHandler, smsHandler
from app import db


# Parser to check that required arguments are sent to add dependant to the database
dependant_put_args = reqparse.RequestParser()
dependant_put_args.add_argument("id_citizen", type=str, help="The ID of the citizen in string format", required=True)
dependant_put_args.add_argument("email", type=str, help="Email is required in string format", required=True)
dependant_put_args.add_argument("name", type=str, help="Name is required in string format", required=True)
dependant_put_args.add_argument("surname", type=str, help="Surname is required in string format", required=True)
dependant_put_args.add_argument("date_of_birth", type=str, help="Date of birth is required in the format YYYY-MM-DD", required=True)
dependant_put_args.add_argument("mobile_num", type=str, help="Mobile number is required in string format", required=True)
dependant_put_args.add_argument("medical_aid", type=str, help="Medical aid number is required to be in string format")
dependant_put_args.add_argument("citizen_address", type=str, help="Address is required in string format")
dependant_put_args.add_argument("parent_id", type=str, help="The ID of the parent in string format", required=True)

# Parser to check that required arguments are sent to get a dependant from the database
dependant_get_args = reqparse.RequestParser()
dependant_get_args.add_argument("parent_id", type=str, help="The ID of the parent in string format", required=True)

# Parser to check that required arguments are sent to update a dependant in the database
dependant_patch_args = reqparse.RequestParser()
dependant_patch_args.add_argument("id_citizen", type=str, help="The ID of the citizen in string format", required=True)
dependant_patch_args.add_argument("email", type=str, help="Email is required in string format")
dependant_patch_args.add_argument("name", type=str, help="Name is required in string format")
dependant_patch_args.add_argument("surname", type=str, help="Surname is required in string format")
dependant_patch_args.add_argument("date_of_birth", type=str, help="Date of birth is required in the format YYYY-MM-DD")
dependant_patch_args.add_argument("mobile_num", type=str, help="Mobile number is required in string format")
dependant_patch_args.add_argument("medical_aid", type=str, help="Medical aid number is required to be in string format")
dependant_patch_args.add_argument("citizen_address", type=str, help="Address is required in string format")
dependant_patch_args.add_argument("parent_id", type=str, help="The ID of the parent in string format")

# Parser to check that required arguments are sent to delete a citizen from the database
dependant_del_args = reqparse.RequestParser()
dependant_del_args.add_argument("id_citizen", type=str, help="The ID of the citizen in string format", required=True)

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
    def get(self):
        args = dependant_get_args.parse_args()
        dataHandler.cleanData(args)
        return getDependant(args), 200

    def put(self):
        args = dependant_put_args.parse_args()
        dataHandler.cleanData(args)
        addDependant(args)
        return { "message": "Added to database" }, 201
    
    def patch(self):
        args = dependant_patch_args.parse_args()
        dataHandler.cleanData(args)
        updateDependant(args)
        return { "message": "Updated the database" }, 200
    
    def delete(self):
        args = dependant_del_args.parse_args()
        deleteDependant(args)
        return { "message": "Deleted from database" }, 204

# Add resource to the API
dependant_api.add_resource(DependantResource, "")

# Get a dependant by their ID and return the full database entry
def getDependant(args):
    result = Citizen.query.filter_by(parent_id=args["parent_id"]).all()
    if result:
        return result
    else:
        abort(404, message="A dependant with this parentID does not exist")

# Add a dependant to the database
def addDependant(args):
    result = Citizen.query.filter_by(id_citizen = args["id_citizen"]).first()
    if result:
        abort(409, message="A dependant with this ID already exists")
    else:
        result = Citizen.query.filter_by(id_citizen = args["parent_id"]).first()
        if result:
            try:
                date = datetime.strptime(args["date_of_birth"], '%Y-%m-%d')
            except ValueError:
                abort(400, message="The date should be in format YYYY-MM-DD")
            new_dependant = Citizen(id_citizen = args["id_citizen"], email = args["email"], name = args["name"],
            surname = args["surname"], date_of_birth = date,
            mobile_num = args["mobile_num"], medical_aid = args["medical_aid"],
            citizen_address = args["citizen_address"], parent_id = args["parent_id"])
            db.session.add(new_dependant)
            db.session.commit()
            smsHandler.sendMockSms("A dependant has been added", result.mobile_num)
        else:
            abort(404, message="A parent with this ID does not exist")

# Update the dependant in the database
def updateDependant(args):
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
            except ValueError:
                abort(400, message="The date should be in format YYYY-MM-DD")
            result.date_of_birth = date
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
def deleteDependant(args):
    result = Citizen.query.filter_by(id_citizen=args["id_citizen"]).first()
    if not result:
        abort(404, message="Dependant with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()
