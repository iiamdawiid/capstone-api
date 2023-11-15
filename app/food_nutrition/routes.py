from . import food_nutrition_blueprint as f
from flask import request
from flask_jwt_extended import jwt_required, current_user
from ..models import FoodNutrition

@f.post('/save_food_nutrition')
@jwt_required()
def handle_save_food_nutrition():
    body = request.json 

    if body is None:
        response = {
            "message": "Invalid request"
        }
        return response, 400
    
    food_name = body.get('food_name')
    serving_size = body.get('serving_size')
    calories = body.get('calories')
    protein = body.get('protein')
    fats = body.get('fats')
    carbs = body.get('carbs')
    
    saved_nutrition = FoodNutrition(
        food_name=food_name, serving_size=serving_size, calories=calories, 
        protein=protein, fats=fats, carbs=carbs, saved_by=current_user.id
        )
    
    saved_nutrition.create()

    response = {
        "message": "food nutrition successfully saved",
        "food_nutrition": saved_nutrition.to_response()
    }
    return response, 201

@f.delete('/delete_foods/<save_id>')
@jwt_required()
def handle_food_delete(save_id):
    saved_food = FoodNutrition.query.filter_by(id=save_id).one_or_none()
    if saved_food is None:
        response = {
            "message": "the saved foods do not exist"
        }
        return response, 404
    
    if saved_food.saved_by != current_user.id:
        response = {
            "message": "can not delete another user's saved foods"
        }
        return response, 401
    
    saved_food.delete()

    response = {
        "message": "saved foods successfully deleted"
    }
    return response, 200