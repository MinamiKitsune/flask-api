from flask_restful import Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
import uuid
from . import vaccination_api
from ..database_models import Location, Vial, Vaccine, Citizen, Vaccination
from .. import data_handler, sms_handler
from app import db

# Parser to check that required arguments are sent to add a vaccination to the database
vaccination_put_args = reqparse.RequestParser()
vaccination_put_args.add_argument("citizen_id", type=str, required=True,
                                  help="The ID number of the citizen is required in String format.")
vaccination_put_args.add_argument("vial_id", type=str, required=True,
                                  help="The vial ID of the vial is required in String format.")
vaccination_put_args.add_argument("location_id", type=int, required=True,
                                  help="The location ID is required in Int format.")
vaccination_put_args.add_argument("date_of_vaccination", type=str, required=True,
                                  help="The date of the vaccination is required, the format should be YYYY-MM-DD")
vaccination_put_args.add_argument("dosage_number", type=int, required=True,
                                  help="The dosage number is required in the Int format.")
vaccination_put_args.add_argument("side_effects", type=bool, required=True,
                                  help="The side effects is required and has to be in Boolean format.")
vaccination_put_args.add_argument("description_side_effects",
                                  type=str, help="Side effects description needs to be in String format.")

# Parser to check that required arguments are sent to get a vaccination from the database
vaccination_get_args = reqparse.RequestParser()
vaccination_get_args.add_argument("id_vaccination", type=str, required=True,
                                  help="The ID of the vaccination is required in String format.")

# Parser to check that required arguments are sent to update a vaccination
vaccination_patch_args = reqparse.RequestParser()
vaccination_patch_args.add_argument("id_vaccination", type=str, required=True,
                                    help="The ID of the vaccination is required in String format.")
vaccination_patch_args.add_argument("dosage_number", type=int,
                                    help="The dosage number need to be in Int format.")
vaccination_patch_args.add_argument("side_effects", type=bool,
                                    help="The side effects has to be in Boolean format.")
vaccination_patch_args.add_argument("description_side_effects", type=str,
                                    help="Side effects description needs to be in String format.")

# Parser to check that required arguments are sent to delete a vaccination
vaccination_del_args = reqparse.RequestParser()
vaccination_del_args.add_argument("id_vaccination", type=str, required=True,
                                  help="The ID of the vaccination is required in String format.")

# Fields to marshal the responses
resource_fields = {
    'id_vaccination': fields.String,
    'citizen_id': fields.String,
    'vial_id': fields.String,
    'location_id': fields.String,
    'date_of_vaccination': fields.String,
    'dosage_number': fields.Integer,
    'side_effects': fields.String,
    'description_side_effects': fields.String,
    'email': fields.String,
    'name': fields.String,
    'surname': fields.String,
    'date_of_birth': fields.String,
    'mobile_num': fields.String,
    'medical_aid': fields.String,
    'citizen_address': fields.String,
    'parent_id': fields.String,
    'vaccine_id': fields.Integer,
    'vaccine_name': fields.String,
    'target_disease': fields.String,
    'number_to_administer': fields.Integer,
    'dosage_interval': fields.Integer,
    'location_address': fields.String,
    'country': fields.String,
    'zip_code': fields.String,
    'name_of_place': fields.String
}


# This class will handle all of the methods related to the vaccination event
# where a citizen will be vaccinated
class VaccinationResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        try:
            args = vaccination_get_args.parse_args()
            data_handler.remove_space(args)
            return get_vaccination(args), 200
        except Exception:
            abort(500, message="An internal server error has occurred, please try again later.")

    def put(self):
        try:
            args = vaccination_put_args.parse_args()
            data_handler.remove_space(args)
            add_vaccination(args)
            return {"message": "Added to database"}, 201
        except Exception:
            abort(500, message="An internal server error has occurred, please try again later.")

    def patch(self):
        try:
            args = vaccination_patch_args.parse_args()
            data_handler.remove_space(args)
            update_vaccination(args)
            return {"message": "Updated the database"}, 200
        except Exception:
            abort(500, message="An internal server error has occurred, please try again later.")

    def delete(self):
        try:
            args = vaccination_del_args.parse_args()
            data_handler.remove_space(args)
            delete_vaccination(args)
            return {"message": "Deleted from database"}, 204
        except Exception:
            abort(500, message="An internal server error has occurred, please try again later.")


# Add the resource to the API
vaccination_api.add_resource(VaccinationResource, "")


# Get a vaccination based on the unique ID of the vaccination
def get_vaccination(args):
    result = db.session.query(
        Vaccination.id_vaccination, Vaccination.citizen_id, Vaccination.vial_id, Vaccination.location_id,
        Vaccination.date_of_vaccination, Vaccination.dosage_number,
        Vaccination.side_effects, Vaccination.description_side_effects,
        Vial.vaccine_id,
        Vaccine.vaccine_name, Vaccine.target_disease, Vaccine.number_to_administer, Vaccine.dosage_interval,
        Citizen.email, Citizen.name, Citizen.surname, Citizen.date_of_birth, Citizen.mobile_num, Citizen.medical_aid,
        Citizen.citizen_address, Citizen.parent_id,
        Location.location_address, Location.country, Location.zip_code, Location.name_of_place
    ).filter_by(id_vaccination=args["id_vaccination"]
                ).join(Vial, Vaccination.vial_id == Vial.id_vial
                       ).join(Vaccine, Vial.vaccine_id == Vaccine.id_vaccine
                              ).join(Citizen, Vaccination.citizen_id == Citizen.id_citizen
                                     ).join(Location, Vaccination.location_id == Location.id_location
                                            ).first()
    if result:
        return result
    else:
        abort(404, message="Vaccination with this ID does not exist")


# Add a vaccination to the database
def add_vaccination(args):
    if args["side_effects"] and args["description_side_effects"] is None:
        abort(400, message="Side effects are true and no description has been given, please add a description")
    else:
        if vial_exists(args):
            exists, mobile = citizen_exists(args)
            if exists:
                if location_exists(args):
                    try:
                        date = datetime.strptime(args["date_of_vaccination"], '%Y-%m-%d')
                        unique_id = create_unique_id()
                        new_vaccination = Vaccination(id_vaccination=unique_id, citizen_id=args["citizen_id"],
                                                      vial_id=args["vial_id"],
                                                      location_id=args["location_id"], date_of_vaccination=date,
                                                      dosage_number=args["dosage_number"],
                                                      side_effects=args["side_effects"],
                                                      description_side_effects=args["description_side_effects"])
                        db.session.add(new_vaccination)
                        db.session.commit()
                        sms_handler.send_mock_vaccination_sms("You have been vaccinated.", mobile, unique_id)
                    except ValueError:
                        abort(400, message="The date should be in format YYYY-MM-DD")


# Update a vaccination
def update_vaccination(args):
    result = Vaccination.query.filter_by(id_vaccination=args["id_vaccination"]).first()
    if not result:
        abort(404, message="A vaccination with this ID does not exist, cannot update")
    else:
        if args["dosage_number"]:
            result.dosage_number = args["dosage_number"]
        if args["side_effects"]:
            result.side_effects = args["side_effects"]
        if args["description_side_effects"]:
            result.description_side_effects = args["description_side_effects"]
        db.session.commit()


# Delete a vaccination
def delete_vaccination(args):
    result = Vaccination.query.filter_by(id_vaccination=args["id_vaccination"]).first()
    if not result:
        abort(404, message="A vaccination with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()


# Creates a unique identifier for a vaccination
def create_unique_id():
    unique = str(uuid.uuid4())
    result = Vaccination.query.filter_by(id_vaccination=unique).first()
    if result:
        return create_unique_id()
    else:
        return unique


# Checks if a vial with the specified ID exists in the database and returns true if it does
def vial_exists(args):
    if Vial.query.filter_by(id_vial=args["vial_id"]).first():
        return True
    else:
        abort(404, message="A vial with this ID does not exist, please make sure the vial has been registered")


# Checks if the citizen exists in the database and returns the mobile number and true if they exist
def citizen_exists(args):
    result = Citizen.query.filter_by(id_citizen=args["citizen_id"]).first()
    if result:
        return True, result.mobile_num
    else:
        abort(404,
              message="Citizen with this ID does not exist, "
                      "please make sure the ID of the citizen has been entered correctly")


# Checks if a location exists in the database and returns true if it does
def location_exists(args):
    if Location.query.filter_by(id_location=args["location_id"]).first():
        return True
    else:
        abort(404,
              message="Location with this ID does not exist, "
                      "please query the locations to find the correct location ID")
