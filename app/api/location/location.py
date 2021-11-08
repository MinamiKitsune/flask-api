from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import location_api
from ..databaseModels import Location
from .. import dataHandler
from app import db


# TODO redo most of this to allow for better integration
#Parser to check that required arguments are sent
location_post_args = reqparse.RequestParser()
location_post_args.add_argument("address", type=str, help="Address is required", required=True)
location_post_args.add_argument("name_of_place", type=str, help="Name of place is required", required=True)

#Fields to marshal the responses
resource_fields = {
    'id_location': fields.Integer,
    'address': fields.String,
    'name_of_place': fields.String,
}

#Class to handle methods related to location
class LocationResource(Resource):
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
        args = location_post_args.parse_args()
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
location_api.add_resource(LocationResource, '/locations/<string:location_id>')
#location list resource
location_api.add_resource(LocationList, '/locations')