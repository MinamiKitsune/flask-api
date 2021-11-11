from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import dependant_api
from ..databaseModels import Citizen
from .. import dataHandler
from app import db

# TODO redo most of this to allow for better integration
#Parser to check that required arguments are sent
dependant_post_args = reqparse.RequestParser()
dependant_post_args.add_argument("email", type=str, help="Email is required", required=True)
dependant_post_args.add_argument("name", type=str, help="Name is required" , required=True)
dependant_post_args.add_argument("surname", type=str, help="Surname is required", required=True)
dependant_post_args.add_argument("date_of_birth", type=str, help="Date of birth is required", required=True)
dependant_post_args.add_argument("mobile_num", type=str, help="Mobile number is required", required=True)
dependant_post_args.add_argument("medical_aid", type=str, required=False)
dependant_post_args.add_argument("address", type=str, help="Address is required", required=True)
dependant_post_args.add_argument("parent_id", type=int, help="Parent ID is required", required=True)

#Parser to check that required arguments are sent to update
dependant_put_args = reqparse.RequestParser()
dependant_put_args.add_argument("email", type=str)
dependant_put_args.add_argument("name", type=str)
dependant_put_args.add_argument("surname", type=str)
dependant_put_args.add_argument("date_of_birth", type=str)
dependant_put_args.add_argument("mobile_num", type=str)
dependant_put_args.add_argument("medical_aid", type=str)
dependant_put_args.add_argument("address", type=str)

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

#Class to handle methods related to dependants
class DependantResource(Resource):
    #Function to retrieve existing dependant
    @marshal_with(resource_fields)
    def get(self, dependant_id):
        dependant = CitizenModel.query.filter_by(id_citizen=dependant_id).first()
        
        if not dependant:
            abort(404, message = "dependant with this ID does not exist")
            
        return dependant

    #Function to create new dependant
    @marshal_with(resource_fields)
    def post(self, dependant_id):
        args = dependant_post_args.parse_args()
        dependant = CitizenModel.query.filter_by(id_citizen=dependant_id).first()
        
        if dependant:
            abort(409, message="dependant ID already exists, cannot add")
        try:
            dependantInfo = CitizenModel(
                                id_citizen=dependant_id,
                                email=args["email"],
                                name=args["name"],
                                surname=args["surname"],
                                date_of_birth=args["date_of_birth"],
                                mobile_num=args["mobile_num"],
                                medical_aid=args["medical_aid"],
                                address=args["address"],
                                parent_id=args["parent_id"]
                            )
            db.session.add(dependantInfo)
            db.session.commit()
            SMS()
            return {"message":"dependant added to database"}, 201

        except Exception as e:
            return 400

    #Function to update certain dependant
    @marshal_with(resource_fields)
    def put(self, dependant_id):
        args = dependant_put_args.parse_args() 
        dependant = CitizenModel.query.filter_by(id_citizen = dependant_id).first()
           
        if not dependant:
            abort(404, message = "dependant with this ID does not exist, cannot update")
        
        if args['email']:
            dependant.email = args['email']
         if args['name']:
            dependant.email = args['name']
         if args['surname']:
            dependant.email = args['surname']
         if args['date_of_birth']:
            dependant.email = args['date_of_birth']
        if args['mobile_num']:
            dependant.mobile_num = args['mobile_num']
        if args['medical_aid']:
            dependant.medical_aid = args['medical_aid']
        if args['address']:
            dependant.address = args['address']
        
        db.session.commit()

        return {"message":"dependant updated"}, 200
    
    #Function to delete dependant
    def delete(self, dependant_id):
        dependant = CitizenModel.query.filter_by(id_citizen = dependant_id).first()
        if not dependant:
            abort(404, message="dependant with this ID does not exist, cannot delete")
        db.session.delete(dependant)
        db.session.commit()

        return {"message":"dependant deleted from database"}, 204

# TODO move this above
class DependantList(Resource):
    #Fuction to retrieve all dependants
    def get(self):
        dependant = CitizenModel.query.all()
        dependantList = {}

        for user in dependant:
            dependantList[user.id_citizen] = {"email":user.email,
                                                "name":user.name,
                                                "surname":user.surname,
                                                "date_of_birth":user.date_of_birth,
                                                "mobile_num":user.mobile_num,
                                                "medical_aid":user.medical_aid,
                                                "address":user.address,
                                                "parent_id":user.parent_id}
        return dependantList

#add resource to the API
#dependant resource
dependant_api.add_resource(DependantResource, '/citizens/dependants/<int:dependant_id>')
#dependant list resource
dependant_api.add_resource(DependantList, '/citizens/dependants')

#Function to send sms notification 
def SMS():
    print("An sms will be sent to you shortly...")
