from flask_restful import Resource, reqparse, abort, fields, marshal_with
from . import location_api
from ..database_models import Location
from .. import data_handler
from app import db

# Parser to check if the required arguments are sent to get location data from the database
location_get_args = reqparse.RequestParser()
location_get_args.add_argument("id_location", type=str,
                               help="The ID of the location in Int format")
location_get_args.add_argument("location_address", type=str,
                               help="The address of the location in String format")
location_get_args.add_argument("country", type=str,
                               help="The country of the location in String format")
location_get_args.add_argument("zip_code", type=str,
                               help="The zip code of the location in String format")
location_get_args.add_argument("name_of_place", type=str,
                               help="The name of the location in String format")

# Parser to check if the required arguments are sent to add a new location to the database
location_put_args = reqparse.RequestParser()
location_put_args.add_argument("location_address", type=str, required=True,
                               help="The address of the location in String format is required")
location_put_args.add_argument("country", type=str, required=True,
                               help="The country of the location in String format is required")
location_put_args.add_argument("zip_code", type=str, required=True,
                               help="The zip code of the location in String format is required")
location_put_args.add_argument("name_of_place", type=str, required=True,
                               help="The name of the location in String format is required")

# Parser to check if the required arguments are sent to update a location in the database
location_patch_args = reqparse.RequestParser()
location_patch_args.add_argument("id_location", type=str, required=True,
                                 help="The ID of the location in Int format is required")
location_patch_args.add_argument("location_address", type=str,
                                 help="The address of the location in String format")
location_patch_args.add_argument("country", type=str,
                                 help="The country of the location in String format")
location_patch_args.add_argument("zip_code", type=str,
                                 help="The zip code of the location in String format")
location_patch_args.add_argument("name_of_place", type=str,
                                 help="The name of the location in String format")

# Parser to check if the required arguments are sent to delete a location from the database
location_del_args = reqparse.RequestParser()
location_del_args.add_argument("id_location", type=str, required=True,
                               help="The ID of the location in Int format is required")

# Fields to marshal the responses
resource_fields = {
    'id_location': fields.Integer,
    'location_address': fields.String,
    'country': fields.String,
    'zip_code': fields.String,
    'name_of_place': fields.String
}


# Class to handle methods related to location
class LocationResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = location_get_args.parse_args()
        data_handler.clean_data(args)
        if data_handler.check_if_empty(args):
            return get_all_locations(), 200
        else:
            return get_location(args), 200

    def put(self):
        args = location_put_args.parse_args()
        data_handler.clean_data(args)
        add_location(args)
        return {"message": "Added to database"}, 201

    def patch(self):
        args = location_patch_args.parse_args()
        data_handler.clean_data(args)
        update_location(args)
        return {"message": "Updated the database"}, 200

    def delete(self):
        args = location_del_args.parse_args()
        data_handler.clean_data(args)
        delete_location(args)
        return {"message": "Deleted from database"}, 204


# Add resource to the API
location_api.add_resource(LocationResource, '')


# Get all of the locations in the database
def get_all_locations():
    return Location.query.all()


# Get a single location from the database based on the arguments provided
def get_location(args):
    if args["id_location"]:
        result = Location.query.filter_by(id_location=args["id_location"]).first()
        if result:
            return result
        else:
            abort(404, message="A location with this ID does not exist")
    elif args["location_address"]:
        search = "%{}%".format(args["location_address"])
        result = Location.query.filter(Location.location_address.like(search)).first()
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
        abort(400,
              message="Not the correct arguments specified; "
                      "only id_location, location_address, country, zip_code or name_of_place can be used")
    abort(404, message="This location does not exist")


# Add a location to the database
def add_location(args):
    result = Location.query.filter_by(location_address=args["location_address"]).first()
    if result:
        abort(409, message="A location with this address already exists")
    else:
        new_location = Location(location_address=args["location_address"], country=args["country"],
                                zip_code=args["zip_code"], name_of_place=args["name_of_place"])
        db.session.add(new_location)
        db.session.commit()


# Update a location in the database
def update_location(args):
    result = Location.query.filter_by(id_location=args["id_location"]).first()
    if not result:
        abort(404, message="Location with this ID does not exist, cannot update")
    else:
        if args["id_location"]:
            result.id_location = args["id_location"]
        if args["location_address"]:
            result.location_address = args["location_address"]
        if args["country"]:
            result.country = args["country"]
        if args["zip_code"]:
            result.zip_code = args["zip_code"]
        if args["name_of_place"]:
            result.name_of_place = args["name_of_place"]
        db.session.commit()


# Delete a location in the database
def delete_location(args):
    result = Location.query.filter_by(id_location=args["id_location"]).first()
    if not result:
        abort(404, message="Location with this ID does not exist, cannot delete")
    else:
        db.session.delete(result)
        db.session.commit()
