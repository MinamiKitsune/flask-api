from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import vaccine_api
from ..databaseModels import Vaccine
from .. import dataHandler
from app import db


# Parser to check if the required arguments are sent
vaccine_put_args = reqparse.RequestParser()
vaccine_put_args.add_argument("vaccine_name", type=str, help="The name of the vaccine is required in String format", required=True)
vaccine_put_args.add_argument("target_disease", type=str, help="The name of the target disease that the vaccine is made for is required in String format", required=True)
vaccine_put_args.add_argument("number_to_administer", type=int, help="The number of dossages the vaccine requires is required in Int format", required=True)
vaccine_put_args.add_argument("dosage_interval", type=int, help="The number of days that need to elapse before the next dose is administered")

# Parser to check if the required arguments are sent to get vaccines data
vaccine_get_args = reqparse.RequestParser()
vaccine_get_args.add_argument("id_vaccine", type=int, help="The ID of the vaccine in Int format")
vaccine_get_args.add_argument("vaccine_name", type=str, help="The name of the vaccine is required in String format")
vaccine_get_args.add_argument("target_disease", type=str, help="The name of the target disease that the vaccine is made for is required in String format")

# Parser to check required arguments are sent to update
vaccine_patch_args = reqparse.RequestParser()
vaccine_patch_args.add_argument("id_vaccine", type=int, help="The ID of the vaccine in Int format", required=True)
vaccine_patch_args.add_argument("vaccine_name", type=str, help="The name of the vaccine is required in String format")
vaccine_patch_args.add_argument("target_disease", type=str, help="The name of the target disease that the vaccine is made for is required in String format")
vaccine_patch_args.add_argument("number_to_administer", type=int, help="The number of dossages the vaccine requires is required in Int format")
vaccine_patch_args.add_argument("dosage_interval", type=int, help="The number of days that need to elapse before the next dose is administered")

# Parser to check required arguments are sent to delete
vaccine_del_args = reqparse.RequestParser()
vaccine_del_args.add_argument("id_vaccine", type=int, help="The ID of the vaccine in Int format", required=True)

# fields to marshal the responses
resource_fields = {
    'id_vaccine': fields.Integer,
    'vaccine_name': fields.String,
    'target_disease': fields.String,
    'number_to_administer': fields.Integer,
    'dosage_interval': fields.Integer
}

# This class will handle all of the methods related to the the vaccines
class VaccineResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = vaccine_get_args.parse_args()
        dataHandler.cleanData(args)
        if dataHandler.checkIfEmpty(args):
            return getAllVaccine(), 200
        else:
            return getVaccine(args), 200
    
    def put(self):
        args = vaccine_put_args.parse_args()
        dataHandler.cleanData(args)
        if args["number_to_administer"] > 1 and args["dosage_interval"] == None:
            abort(400, message="A number of dosages greater than 1 is specified with no dosage interval, please add a dosage interval")
        else:
            addVaccine(args)
        return { "message": "Added to database" }, 201
    
    def patch(self):
        args = vaccine_patch_args.parse_args()
        dataHandler.cleanData(args)
        updateVaccine(args)
        return { "message": "Updated the database" }, 200
    
    def delete(self):
        args = vaccine_patch_args.parse_args()
        deleteVaccine(args)
        return { "message": "Deleted from database" }, 204


# Add the resource to the API
vaccine_api.add_resource(VaccineResource, '')

# Add vaccine to database
def addVaccine(args):
    new_vaccine = Vaccine(vaccine_name = args["vaccine_name"], target_disease = args["target_disease"], number_to_administer = args["number_to_administer"],
    dosage_interval = args["dosage_interval"])
    db.session.add(new_vaccine)
    db.session.commit()

# Get all of the vaccines from the database
def getAllVaccine():
    return Vaccine.query.all()

# Get a specific vaccine or set of vaccines from database
def getVaccine(args):
    if args["id_vaccine"]:
        result = Vaccine.query.filter_by(id_vaccine=args["id_vaccine"]).first()
        if result:
            return result
        else:
            abort(404, message="Vaccine with this ID does not exist")
    elif args["vaccine_name"]:
        result = Vaccine.query.filter_by(vaccine_name=args["vaccine_name"]).all()
        if result:
            return result
        else:
            abort(404, message="Vaccine with this name does not exist")
    elif args["target_disease"]:
        result = Vaccine.query.filter_by(target_disease=args["target_disease"]).all()
        if result:
            return result
        else:
            abort(404, message="Vaccine with this target disease does not exist")
    else:
        abort(400, message="Not the correct arguments specified; only id_vaccine, vaccine_name or target_disease can be used")

# update the database
def updateVaccine(args):
    result = Vaccine.query.filter_by(id_vaccine=args["id_vaccine"]).first()
    if not result:
        abort(404, message="Vaccine with this ID does not exist, cannot update")
    else:
        if args["vaccine_name"]:
            result.vaccine_name = args["vaccine_name"]
        if args["target_disease"]:
            result.target_disease = args["target_disease"]
        if args["number_to_administer"]:
            result.number_to_administer = args["number_to_administer"]
        if args["dosage_interval"]:
            result.dosage_interval = args["dosage_interval"]
        db.session.commit()

# delete from the database
def deleteVaccine(args):
    result = Vaccine.query.filter_by(id_vaccine=args["id_vaccine"]).first()
    if not result:
        abort(404, message="Vaccine with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()