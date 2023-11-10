from flask import Blueprint

calorie_calculator_blueprint = Blueprint('calorie_calculator', __name__, url_prefix='/bmrcalculator')

from . import routes    