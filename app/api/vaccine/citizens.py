from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaccine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Citizen table model
class CitizenModel(db.Model):
   id_citizen = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(50), nullable=False)
   name = db.Column(db.String(30), nullable=False)
   surname = db.Column(db.String(30), nullable=False)
   date_of_birth = db.Column(db.String, nullable=False)
   mobile_num = db.Column(db.String(10), nullable=False)
   medical_aid = db.Column(db.String(20), nullable=True)
   address = db.Column(db.String(45), nullable=False )
   parent_id = db.Column(db.Integer, nullable=True)

#Parser to check that required arguments are sent
citizenPostArgs = reqparse.RequestParser()
citizenPostArgs.add_argument("email", type=str, help="Email is required", required=True)
citizenPostArgs.add_argument("name", type=str, help="Name is required", required=True)
citizenPostArgs.add_argument("surname", type=str, help="Surname is required", required=True)
citizenPostArgs.add_argument("date_of_birth", type=str, help="Date of birth is required", required=True)
citizenPostArgs.add_argument("mobile_num", type=str, help="Mobile number is required", required=True)
citizenPostArgs.add_argument("medical_aid", type=str, required=False)
citizenPostArgs.add_argument("address", type=str, help="Address is required", required=True)
citizenPostArgs.add_argument("parent_id", type=int, required=False)

#Parser to check that required arguments are sent to update
citizenPutArgs = reqparse.RequestParser()
citizenPutArgs.add_argument("medical_aid", type=str)

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

#Function to send sms notification 
def SMS(): 
    print("An sms will be sent to you shortly...")

#Class to handle methods related to citizens
class Citizen(Resource):
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
        args = citizenPostArgs.parse_args()
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
        args = citizenPutArgs.parse_args()
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
api.add_resource(Citizen, "/citizens/<int:citizen_id>")
#dependent list resource
api.add_resource(CitizensList, "/citizens")  

if __name__ == "__main__":
    app.run(debug=True)        