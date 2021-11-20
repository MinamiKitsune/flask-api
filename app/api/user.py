import uuid
from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource, reqparse, abort
from werkzeug.security import check_password_hash, generate_password_hash
from . import user_api
from . import data_handler
from .database_models import User
from .decorator import token_required
from .. import app, db
import jwt

# Parser to check that required arguments are sent to add a user to the database
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("username", type=str, required=True,
                           help="The username of the user is required. The argument should be a String.")
user_put_args.add_argument("password", type=str, required=True,
                           help="The password of the user is required. The argument should be a String.")


# This class is used to test the connection to the API
class LoginResource(Resource):
    def get(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            abort(400, message="Login details required.")
        user = User.query.filter_by(username=auth.username).first()
        if not user:
            abort(400, message="Login details are wrong.")
        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=60)},
                app.config['SECRET_KEY'])
            return {'token': token.decode('UTF-8')}
        abort(400, message="Login details are wrong.")


class UserResource(Resource):
    def put(self):
        args = user_put_args.parse_args()
        data_handler.remove_space(args)
        add_user(args, "user")
        return {"message": "Added to database"}, 201


class AdminResource(Resource):
    @token_required
    def put(self):
        if data_handler.check_if_admin(request.headers['x-access-token']):
            args = user_put_args.parse_args()
            data_handler.remove_space(args)
            add_user(args, "admin")
            return {"message": "Added to database"}, 201
        else:
            abort(403, message="Forbidden.")


# Add the resources to the API
user_api.add_resource(LoginResource, '/login')
user_api.add_resource(AdminResource, "/admin")
user_api.add_resource(UserResource, '')


def add_user(args, user_class):
    result = User.query.filter_by(username=args["username"]).first()
    if result:
        abort(409, message="A user with this username already exists")
    else:
        hashed_password = generate_password_hash(args['password'], method='sha256')
        if user_class == "admin":
            new_user = User(public_id=str(uuid.uuid4()), username=args['username'], password=hashed_password,
                            admin=True)
        else:
            new_user = User(public_id=str(uuid.uuid4()), username=args['username'], password=hashed_password,
                            admin=False)
        db.session.add(new_user)
        db.session.commit()
