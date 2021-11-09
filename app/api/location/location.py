from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import location_api
from ..databaseModels import Location
from .. import dataHandler
from app import db


# Parser to check if the required arguments are sent to get location data
location_get_args = reqparse.RequestParser()
location_get_args.add_argument("id_location", type=str, help="The ID of the location in Int format")
location_get_args.add_argument("address", type=str, help="The address of the location in String format")
location_get_args.add_argument("country", type=str, help="The country of the location in String format")
location_get_args.add_argument("zip_code", type=str, help="The zip code of the location in String format")
location_get_args.add_argument("name_of_place", type=str, help="The name of the location in String format")

# Parser to check if the required arguments are sent to add a new location
location_put_args = reqparse.RequestParser()
location_put_args.add_argument("address", type=str, help="The address of the location in String format is required", required=True)
location_put_args.add_argument("country", type=str, help="The country of the location in String format is required", required=True)
location_put_args.add_argument("zip_code", type=str, help="The zip code of the location in String format is required", required=True)
location_put_args.add_argument("name_of_place", type=str, help="The name of the location in String format is required", required=True)

# Parser to check if the required arguments are sent to update a location
location_patch_args = reqparse.RequestParser()
location_patch_args.add_argument("id_location", type=str, help="The ID of the location in Int format is required", required=True)
location_patch_args.add_argument("address", type=str, help="The address of the location in String format")
location_patch_args.add_argument("country", type=str, help="The country of the location in String format")
location_patch_args.add_argument("zip_code", type=str, help="The zip code of the location in String format")
location_patch_args.add_argument("name_of_place", type=str, help="The name of the location in String format")

# Parser to check if the required arguments are sent to delete a location
location_del_args = reqparse.RequestParser()
location_del_args.add_argument("id_location", type=str, help="The ID of the location in Int format is required", required=True)

#Fields to marshal the responses
resource_fields = {
    'id_location' : fields.Integer,
    'address' : fields.String,
    'country' : fields.String,
    'zip_code' : fields.String,
    'name_of_place' : fields.String
}

#Class to handle methods related to location
class LocationResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = location_get_args.parse_args()
        dataHandler.cleanData(args)
        if dataHandler.checkIfEmpty(args):
            return getAllLocations(), 200
        else:
            return getLocation(args), 200
    
    def put(self):
        args = location_put_args.parse_args()
        dataHandler.cleanData(args)
        addLocation(args)
        return { "message": "Added to database" }, 201
    
    def patch(self):
        args = location_patch_args.parse_args()
        dataHandler.cleanData(args)
        updateLocation(args)
        return { "message": "Updated the database" }, 200
    
    def delete(self):
        args = location_del_args.parse_args()
        deleteLocation(args)
        return { "message": "Deleted from database" }, 204

#add resource to the API
location_api.add_resource(LocationResource, '')

def getAllLocations():
    return Location.query.all()

def getLocation(args):
    if args["id_location"]:
        result = Location.query.filter_by(id_location=args["id_location"]).first()
        if result:
            return result
        else:
            abort(404, message="A location with this ID does not exist")
    elif args["address"]:
        search = "%{}%".format(args["address"])
        result = Location.query.filter(Location.address.like(search)).first()
        if result:
            return result
        else:
            abort(404, message="A location with this address does not exist")
    elif args["country"]:
        search = "%{}%".format(args["country"])
        result = Location.query.filter(Location.country.like(search)).all()
        if result:
            return result
        else:
            abort(404, message="Locations in this country does not exist")
    elif args["zip_code"]:
        search = "%{}%".format(args["zip_code"])
        result = Location.query.filter(Location.zip_code.like(search)).all()
        if result:
            return result
        else:
            abort(404, message="Locations with this zip code does not exist")
    elif args["name_of_place"]:
        search = "%{}%".format(args["name_of_place"])
        result = Location.query.filter(Location.name_of_place.like(search)).first()
        if result:
            return result
        else:
            abort(404, message="A location with this name does not exist")
    else:
        abort(400, message="Not the correct arguments specified; only id_location, address, country, zip_code or name_of_place can be used")

def addLocation(args):
    result = Location.query.filter_by(address = args["address"]).first()
    if result:
        abort(409, message="A location with this address already exists")
    else:
        new_location = Location(address = args["address"], country = args["country"],
        zip_code = args["zip_code"], name_of_place = args["name_of_place"])
        db.session.add(new_location)
        db.session.commit()

def updateLocation(args):
    result = Location.query.filter_by(id_location=args["id_location"]).first()
    if not result:
        abort(404, message="Location with this ID does not exist, cannot update")
    else:
        if args["id_location"]:
            result.id_location = args["id_location"]
        if args["address"]:
            result.address = args["address"]
        if args["country"]:
            result.country = args["country"]
        if args["zip_code"]:
            result.zip_code = args["zip_code"]
        if args["name_of_place"]:
            result.name_of_place = args["name_of_place"]
        db.session.commit()

def deleteLocation(args):
    result = Location.query.filter_by(id_location=args["id_location"]).first()
    if not result:
        abort(404, message="Location with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()