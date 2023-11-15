from . import onerepmax_blueprint as m
from flask import request 
from flask_jwt_extended import jwt_required, current_user
from ..models import OneRepMax

@m.post('/save_onerepmax')
@jwt_required()
def handle_save_max():
    body = request.json

    if body is None:
        response = {
            "message": "Invalid request"
        }
        return response, 400
    
    type_of_lift = body.get('type_of_lift')
    weight = body.get('weight')
    reps = body.get('reps')
    units = body.get('units')
    one_rep_max = body.get('one_rep_max')
    percentage1 = body.get('percentage1')
    percentage2 = body.get('percentage2')
    percentage3 = body.get('percentage3')
    percentage4 = body.get('percentage4')
    percentage5 = body.get('percentage5')
    percentage6 = body.get('percentage6')
    percentage7 = body.get('percentage7')
    percentage8 = body.get('percentage8')

    saved_max = OneRepMax(
        type_of_lift=type_of_lift, weight=weight, reps=reps, units=units, 
        one_rep_max=one_rep_max, percentage1=percentage1, percentage2=percentage2,
        percentage3=percentage3, percentage4=percentage4, percentage5=percentage5,
        percentage6=percentage6,percentage7=percentage7, percentage8=percentage8,
        saved_by=current_user.id
        )
    
    saved_max.create()

    response = {
        "message": "Max successfully saved",
        "max": saved_max.to_response()
    }
    return response, 201

@m.delete('/delete_onerepmax/<save_id>')
@jwt_required()
def handle_delete_max(save_id):
    saved_max = OneRepMax.query.filter_by(id=save_id).one_or_none()

    if saved_max is None:
        response = {
            "message": "saved max does not exist"
        }
    
    if saved_max.saved_by != current_user.id:
        response = {
            "message": "can not delete another user's saved max"
        }
        return response, 401
    
    saved_max.delete()

    response = {
        "message": "saved max successfully deleted"
    }
    return response, 20

@m.get('/saved_maxes')
@jwt_required()
def handle_get_saved_maxes():
    saved_maxes = OneRepMax.query.filter_by(saved_by=current_user.id).all()
    response = {
        "message": "user's saved maxes",
        "saved_maxes": [orm.to_response() for orm in saved_maxes]
    }
    return response, 200