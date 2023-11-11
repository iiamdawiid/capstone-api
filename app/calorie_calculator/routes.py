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
            "message": "Invalid request"
        }
        return response, 400
    
    gender = body.get('gender')
    activity_level = body.get('activity_level')
    weight = body.get('weight')
    height = body.get('height')
    age = body.get('age')
    units = body.get('units')
    calories = body.get('calories')
    gain_weight1 = body.get('gain_weight1')
    gain_weight2 = body.get('gain_weight2')
    gain_weight3 = body.get('gain_weight3')
    lose_weight1 = body.get('lose_weight1')
    lose_weight2 = body.get('lose_weight2')
    lose_weight3 = body.get('lose_weight3')

    saved_calories = CalorieCalculator(
        gender=gender, activity_level=activity_level, weight=weight, height=height, 
        age=age, units=units, calories=calories, gain_weight1=gain_weight1, gain_weight2=gain_weight2, 
        gain_weight3=gain_weight3, lose_weight1=lose_weight1, lose_weight2=lose_weight2, 
        lose_weight3=lose_weight3, saved_by=current_user.id
        )
    
    saved_calories.create()

    response = {
        "message": "calories successfully saved",
        "calories": saved_calories.to_response()
    }
    return response, 201


@c.delete('/delete_calories/<save_id>')
@jwt_required()
def handle_calorie_delete(save_id):
    saved_calories = CalorieCalculator.query.filter_by(id=save_id).one_or_none()
    if saved_calories is None:
        response = {
            "message": "the saved calories do not exist"
        }
        return response, 404
    
    if saved_calories.saved_by != current_user.id:
        response = {
            "message": "can not delete another user's saved calories"
        }
        return response, 401
    
    saved_calories.delete()

    response = {
        "message": "saved calories successfully deleted"
    }
    return response, 200 