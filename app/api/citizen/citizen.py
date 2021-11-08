from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import citizen_api
from ..databaseModels import Citizen
from .. import dataHandler
from app import db

# TODO redo most of this to allow for better integration
#Parser to check that required arguments are sent
citizen_post_args = reqparse.RequestParser()
citizen_post_args.add_argument("email", type=str, help="Email is required", required=True)
citizen_post_args.add_argument("name", type=str, help="Name is required", required=True)
citizen_post_args.add_argument("surname", type=str, help="Surname is required", required=True)
citizen_post_args.add_argument("date_of_birth", type=str, help="Date of birth is required", required=True)
citizen_post_args.add_argument("mobile_num", type=str, help="Mobile number is required", required=True)
citizen_post_args.add_argument("medical_aid", type=str, required=False)
citizen_post_args.add_argument("address", type=str, help="Address is required", required=True)
citizen_post_args.add_argument("parent_id", type=int, required=False)

#Parser to check that required arguments are sent to update
citizen_put_args = reqparse.RequestParser()
citizen_put_args.add_argument("medical_aid", type=str)

#Fields to marshal the responses
resource_fields = {
        'id_citizen': fields.Integer,
        'email': fields.String,
        'name': fields.String,
        'surname': fields.String,
        'date_of_birth': fields.String,
        'medical_aid': fields.String,
        'address': fields.String,
        'parent_id': fields.Integer,
}

#Class to handle methods related to citizens
class CitizenResource(Resource):
    #Function to retrieve existing citizen
    @marshal_with(resource_fields)
    def get(self, citizen_id):
        citizen = CitizenModel.query.filter_by(id_citizen = citizen_id).first()

        if not citizen:
           abort(404, message = "Citizen with this ID does not exist")
        return citizen

    #Function to create new citizen     
    @marshal_with(resource_fields)
    def post(self, citizen_id):
        args = citizen_post_args.parse_args()
        citizen = CitizenModel.query.filter_by(id_citizen=citizen_id).first()

        if citizen:
            abort(409, message = "Citizen ID Taken")
        try:
            citizenInfo = CitizenModel(
                                id_citizen=citizen_id,
                                email=args['email'],
                                name=args['name'],
                                surname=args['surname'],
                                date_of_birth=args['date_of_birth'],
                                mobile_num=args['mobile_num'],
                                medical_aid=args['medical_aid'],
                                address=args['address'],
                                parent_id=args['parent_id']
                            )
            db.session.add(citizenInfo)
            db.session.commit()
            SMS()

            return citizenInfo, 201

        except Exception as e:
            return 400  

    #Function to update citizen medical aid 
    @marshal_with(resource_fields)
    def put(self, citizen_id):
        args = citizen_put_args.parse_args()
        citizen = CitizenModel.query.filter_by(id_citizen=citizen_id).first()
    
        if not citizen:
            abort(404, messaege = "Citizen with this ID does not exist, cannot update")

        if args['medical_aid']:
            citizen.medical_aid = args['medical_aid']

        db.session.commit()

        return {"message": "Citizen updated"}, 200

#Class to handle methods related to citizena
class CitizensList(Resource):
    #Fuction to retrieve all citizens
    def get(self):
        citizen = CitizenModel.query.all()
        citizensList = {}

        for user in citizen:
            citizensList[user.id_citizen] = {"email": user.email,
                                                "name":user.name,
                                                "surname":user.surname,
                                                "date_of_birth": user.date_of_birth,
                                                "mobile_num": user.mobile_num,
                                                "medical_aid": user.medical_aid,
                                                "address": user.address,
                                                "parent_id": user.parent_id} 
        return citizensList

#add resource to the API
#dependent resource
citizen_api.add_resource(CitizenResource, "/citizens/<int:citizen_id>")
#dependent list resource
citizen_api.add_resource(CitizensList, "/citizens")  

#Function to send sms notification 
def SMS(): 
    print("An sms will be sent to you shortly...")  