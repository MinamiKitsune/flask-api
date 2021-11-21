from functools import wraps
from flask import request
import jwt
from .. import app

# Create the decorator to check if the token is passed in the header
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'A Token has not been provided, please login and collect a token'}, 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            return {'message': 'Token is invalid!'}, 401
        return f(*args, **kwargs)

    return decorated
