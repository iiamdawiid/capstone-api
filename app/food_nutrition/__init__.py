from flask import Blueprint

food_nutrition_blueprint = Blueprint('food_nutrition', __name__, url_prefix='/foodnutrition')

from . import routes