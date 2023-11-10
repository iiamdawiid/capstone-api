from . import calorie_calculator_blueprint as c
from flask import request
from flask_jwt_extended import jwt_required, current_user
from ..models import CalorieCalculator

@c.post('/save_calories')
@jwt_required()
def handle_save_calories():
    body = request.json

    if body is None:
        response = {
            "message": "invalid request"
        }
        return response, 400
    
    gender = body.get('gender')
    activity_level = body.get('activity_level')
    weight = body.get('weight')
    height = body.get('height')
    age = body.get('age')
    saved_by = body.get('saved_by')

    saved_calories = CalorieCalculator(gender=gender, activity_level=activity_level, weight=weight, height=height, age=age, saved_by=saved_by)
    saved_calories.create()

    response = {
        "message": "calories successfully saved",
        "calories": saved_calories.to_response()
    }
    return response, 201