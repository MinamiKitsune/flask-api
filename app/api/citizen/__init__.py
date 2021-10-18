from flask import Blueprint
from flask_restful import Api

citizen_BP = Blueprint('citizen', __name__, url_prefix='/citizen')
dependant_BP = Blueprint('dependant', __name__, url_prefix='/dependant')
citizen_BP.register_blueprint(dependant_BP)
dependant_api = Api(dependant_BP)
citizen_api = Api(citizen_BP)

from . import citizen
from . import dependant