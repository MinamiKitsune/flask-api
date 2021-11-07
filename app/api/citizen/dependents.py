from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaccine.db'

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
    parent_id = db.Column(db.Integer, nullable=False)

#Parser to check that required arguments are sent
dependentPostArgs = reqparse.RequestParser()
dependentPostArgs.add_argument("email", type=str, help="Email is required", required=True)
dependentPostArgs.add_argument("name", type=str, help="Name is required" , required=True)
dependentPostArgs.add_argument("surname", type=str, help="Surname is required", required=True)
dependentPostArgs.add_argument("date_of_birth", type=str, help="Date of birth is required", required=True)
dependentPostArgs.add_argument("mobile_num", type=str, help="Mobile number is required", required=True)
dependentPostArgs.add_argument("medical_aid", type=str, required=False)
dependentPostArgs.add_argument("address", type=str, help="Address is required", required=True)
dependentPostArgs.add_argument("parent_id", type=int, help="Parent ID is required", required=True)

#Parser to check that required arguments are sent to update
dependentPutArgs = reqparse.RequestParser()
dependentPutArgs.add_argument("email", type=str)
dependentPutArgs.add_argument("mobile_num", type=str)
dependentPutArgs.add_argument("medical_aid", type=str)
dependentPutArgs.add_argument("address", type=str)

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

#Class to handle methods related to dependents
class Dependent(Resource):
    #Function to retrieve existing dependent
    @marshal_with(resource_fields)
    def get(self, dependent_id):
        dependent = CitizenModel.query.filter_by(id_citizen=dependent_id).first()
        
        if not dependent:
            abort(404, message = "Dependent with this ID does not exist")
            
        return dependent

    #Function to create new dependent
    @marshal_with(resource_fields)
    def post(self, dependent_id):
        args = dependentPostArgs.parse_args()
        dependent = CitizenModel.query.filter_by(id_citizen=dependent_id).first()
        
        if dependent:
            abort(409, message="Dependent ID already exists, cannot add")
        try:
            dependentInfo = CitizenModel(
                                id_citizen=dependent_id,
                                email=args["email"],
                                name=args["name"],
                                surname=args["surname"],
                                date_of_birth=args["date_of_birth"],
                                mobile_num=args["mobile_num"],
                                medical_aid=args["medical_aid"],
                                address=args["address"],
                                parent_id=args["parent_id"]
                            )
            db.session.add(dependentInfo)
            db.session.commit()
            SMS()
            return {"message":"Dependent added to database"}, 201

        except Exception as e:
            return 400

    #Function to update certain dependent
    @marshal_with(resource_fields)
    def put(self, dependent_id):
        args = dependentPutArgs.parse_args() 
        dependent = CitizenModel.query.filter_by(id_citizen = dependent_id).first()
           
        if not dependent:
            abort(404, message = "Dependent with this ID does not exist, cannot update")
        
        if args['email']:
            dependent.email = args['email']
        if args['mobile_num']:
            dependent.mobile_num = args['mobile_num']
        if args['medical_aid']:
            dependent.medical_aid = args['medical_aid']
        if args['address']:
            dependent.address = args['address']
        
        db.session.commit()

        return {"message":"Dependent updated"}, 200
    
    #Function to delete dependent
    def delete(self, dependent_id):
        dependent = CitizenModel.query.filter_by(id_citizen = dependent_id).first()
        if not dependent:
            abort(404, message="Dependent with this ID does not exist, cannot delete")
        db.session.delete(dependent)
        db.session.commit()

        return {"message":"Dependent deleted from database"}, 204

#Class to handle methods related to dependents
class DependentList(Resource):
    #Fuction to retrieve all dependents
    def get(self):
        dependent = CitizenModel.query.all()
        dependentList = {}

        for user in dependent:
            dependentList[user.id_citizen] = {"email":user.email,
                                                "name":user.name,
                                                "surname":user.surname,
                                                "date_of_birth":user.date_of_birth,
                                                "mobile_num":user.mobile_num,
                                                "medical_aid":user.medical_aid,
                                                "address":user.address,
                                                "parent_id":user.parent_id}
        return dependentList

#add resource to the API
#dependent resource
api.add_resource(Dependent, '/citizens/dependents/<int:dependent_id>')
#dependent list resource
api.add_resource(DependentList, '/citizens/dependents')  

if __name__ == "__main__":
    app.run(debug=True)        