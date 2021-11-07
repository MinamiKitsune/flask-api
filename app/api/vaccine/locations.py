from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaccine.db'
db = SQLAlchemy(app)

#Location table model
class LocationModel(db.Model):
    id_location = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(45), nullable=False)
    name_of_place = db.Column(db.String(45), nullable=False)

#Parser to check that required arguments are sent
locationPostArgs = reqparse.RequestParser()
locationPostArgs.add_argument("address", type=str, help="Address is required", required=True)
locationPostArgs.add_argument("name_of_place", type=str, help="Name of place is required", required=True)

#Fields to marshal the responses
resource_fields = {
    'id_location': fields.Integer,
    'address': fields.String,
    'name_of_place': fields.String,
}

#Class to handle methods related to location
class Location(Resource):
    #Function to retrieve existing location
    @marshal_with(resource_fields)
    def get(self, location_id):
        location = LocationModel.query.filter_by(address = location_id).first()
        
        if not location:
            abort(404, message = "Location with this address does not exist")
        return location

    #Function to retrieve existing location
    @marshal_with(resource_fields)
    def post(self, location_id): 
        args = locationPostArgs.parse_args()
        location = LocationModel.query.filter_by(id_location = location_id).first()
        
        if location:
            abort(409, message= "Location with this ID already exists, cannot add")    
        try:
            locationInfo = LocationModel(
                                id_location=location_id,
                                address=args["address"],
                                name_of_place=args["name_of_place"],
                            )

            db.session.add(locationInfo)
            db.session.commit()
            return {"message":"Added to database"}, 201

        except Exception as e:
            return 400

#Class to handle methods related to location
class LocationList(Resource):
    #Fuction to retrieve available locations
    def get(self):
        location = LocationModel.query.all()
        locationList = {}

        for place in location:
            locationList[place.id_location] = {"address": place.address,
                                                "name_of_place": place.name_of_place}
        
        return locationList

#add resource to the API
#location resource
api.add_resource(Location, '/locations/<string:location_id>')
#location list resource
api.add_resource(LocationList, '/locations')  

if __name__ == "__main__":
    app.run(debug=True)        