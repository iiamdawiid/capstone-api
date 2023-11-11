from flask import Blueprint 

onerepmax_blueprint = Blueprint('onerepmax', __name__, url_prefix='/onerepmax')

from . import routes