from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import vaccine_api
from ..database_models import Vaccine
from .. import data_handler
from app import db


# Parser to check if the required arguments are sent to add a vaccine to the database
vaccine_put_args = reqparse.RequestParser()
vaccine_put_args.add_argument("vaccine_name", type=str, required=True,
help="The name of the vaccine is required in String format.")
vaccine_put_args.add_argument("target_disease", type=str, required=True,
help="The name of the target disease that the vaccine is made for is required in String format.")
vaccine_put_args.add_argument("number_to_administer", type=int, required=True,
help="The number of dossages the vaccine requires is required in Int format.")
vaccine_put_args.add_argument("dosage_interval", type=int,
help="The number of days that need to elapse before the next dose is administered.")

# Parser to check if the required arguments are sent to get vaccines data
vaccine_get_args = reqparse.RequestParser()
vaccine_get_args.add_argument("id_vaccine", type=int,
help="The ID of the vaccine needs to be Int format.")
vaccine_get_args.add_argument("vaccine_name", type=str,
help="The name of the vaccine needs to be in String format.")
vaccine_get_args.add_argument("target_disease", type=str,
help="The name of the target disease that the vaccine is made for needs to be in String format.")

# Parser to check required arguments are sent to update a vaccine in the database
vaccine_patch_args = reqparse.RequestParser()
vaccine_patch_args.add_argument("id_vaccine", type=int, required=True,
help="The ID of the vaccine in Int format is required.")
vaccine_patch_args.add_argument("vaccine_name", type=str,
help="The name of the vaccine needs to be in String format.")
vaccine_patch_args.add_argument("target_disease", type=str,
help="The name of the target disease that the vaccine is made for needs to be in String format.")
vaccine_patch_args.add_argument("number_to_administer", type=int,
help="The number of dossages the vaccine requires needs to be in Int format.")
vaccine_patch_args.add_argument("dosage_interval", type=int,
help="The number of days that need to elapse before the next dose is administered needs to be in Int format.")

# Parser to check required arguments are sent to delete a vaccine from the database
vaccine_del_args = reqparse.RequestParser()
vaccine_del_args.add_argument("id_vaccine", type=int, required=True,
help="The ID of the vaccine in Int format is required.")

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
        try:
            args = vaccine_get_args.parse_args()
            data_handler.clean_data(args)
            if data_handler.check_if_empty(args):
                return getAllVaccine(), 200
            else:
                return getVaccine(args), 200
        except Exception:
            abort(500, message="An internal server error has occured, please try again later.")
    
    def put(self):
        try:
            args = vaccine_put_args.parse_args()
            data_handler.clean_data(args)
            if args["number_to_administer"] > 1 and args["dosage_interval"] == None:
                abort(400, message="A number of dosages greater than 1 is specified with no dosage interval, please add a dosage interval")
            else:
                addVaccine(args)
            return { "message": "Added to database" }, 201
        except Exception:
            abort(500, message="An internal server error has occured, please try again later.")
    
    def patch(self):
        try:
            args = vaccine_patch_args.parse_args()
            data_handler.clean_data(args)
            updateVaccine(args)
            return { "message": "Updated the database" }, 200
        except Exception:
            abort(500, message="An internal server error has occured, please try again later.")
    
    def delete(self):
        try:
            args = vaccine_patch_args.parse_args()
            data_handler.clean_data(args)
            deleteVaccine(args)
            return { "message": "Deleted from database" }, 204
        except Exception:
            abort(500, message="An internal server error has occured, please try again later.")


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
        search = "%{}%".format(args["vaccine_name"])
        result = Vaccine.query.filter(Vaccine.vaccine_name.like(search)).all()
        if result:
            return result
        else:
            abort(404, message="Vaccine with this name does not exist")
    elif args["target_disease"]:
        search = "%{}%".format(args["target_disease"])
        result = Vaccine.query.filter(Vaccine.target_disease.like(search)).all()
        if result:
            return result
        else:
            abort(404, message="Vaccine with this target disease does not exist")
    else:
        abort(400, message="Not the correct arguments specified; only id_vaccine, vaccine_name or target_disease can be used")

# Update a vaccine in the database
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

# Delete from the database
def deleteVaccine(args):
    result = Vaccine.query.filter_by(id_vaccine=args["id_vaccine"]).first()
    if not result:
        abort(404, message="Vaccine with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()
