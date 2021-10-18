from flask import Blueprint
from flask_restful import Api

vaccine_BP = Blueprint('vaccine', __name__, url_prefix='/vaccine')
vile_BP = Blueprint('vile', __name__, url_prefix='/vile')
vaccine_BP.register_blueprint(vile_BP)
vile_api = Api(vile_BP)
vaccine_api = Api(vaccine_BP)

from . import vaccine
from . import vile