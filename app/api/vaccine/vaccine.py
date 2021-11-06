from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import vaccine_api
from ..databaseModels import Vaccine
from app import db

# Parser to check if the required arguments are sent
vaccine_put_args = reqparse.RequestParser()
vaccine_put_args.add_argument("vaccine_name", type=str, help="The name of the vaccine is required in String format", required=True)
vaccine_put_args.add_argument("target_disease", type=str, help="The name of the target disease that the vaccine is made for is required in String format", required=True)
vaccine_put_args.add_argument("number_to_administer", type=int, help="The number of dossages the vaccine requires is required in Int format", required=True)
vaccine_put_args.add_argument("dosage_interval", type=int, help="The number of days that need to elapse before the next dose is administered")

# 
vaccine_get_args = reqparse.RequestParser()
vaccine_get_args.add_argument("id_vaccine", type=int, help="The ID of the vaccine in Int format")
vaccine_get_args.add_argument("vaccine_name", type=str, help="The name of the vaccine is required in String format")
vaccine_get_args.add_argument("target_disease", type=str, help="The name of the target disease that the vaccine is made for is required in String format")

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
        if args is None:
            return getFromDatabase()
        else:
            return getFromDatabase(args)
    
    def put(self):
        args = vaccine_put_args.parse_args()
        print(type(args))
        if args["number_to_administer"] > 1 and args["dosage_interval"] == None:
            abort(400, message="A number of dosages greater than 1 is specified with no dosage interval, please add a dosage interval")
        else:
            addToDatabase(args)
        return {"response" : "added vaccine"}, 201

# Add the resource to the API
vaccine_api.add_resource(VaccineResource, '/')

def addToDatabase(args):
    cleanData(args)
    new_vaccine = Vaccine(vaccine_name = args["vaccine_name"], target_disease = args["target_disease"], number_to_administer = args["number_to_administer"],
    dosage_interval = args["dosage_interval"])
    db.session.add(new_vaccine)
    db.session.commit()

def getFromDatabase():
    return Vaccine.query.all()

def getFromDatabase(args):
    cleanData(args)
    if args["id_vaccine"]:
        return Vaccine.query.filter_by(id_vaccine=args["id_vaccine"]).first()
    elif args["vaccine_name"]:
        return Vaccine.query.filter_by(vaccine_name=args["vaccine_name"]).all()
    elif args["target_disease"]:
        return Vaccine.query.filter_by(target_disease=args["target_disease"]).all()

    return Vaccine.query.all()

def cleanData(args):
    for x in args:
        if isinstance(args[x], str):
            args[x] = str(args[x]).lower().strip()