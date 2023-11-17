from . import auth_blueprint as auth
from flask import request, make_response
from flask_jwt_extended import create_access_token, current_user, jwt_required
from werkzeug.security import generate_password_hash
from datetime import timedelta
from ..models import User, CalorieCalculator, OneRepMax, FoodNutrition
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

@auth.post('/register')
def handle_register():
    body = request.json

    if body is None:
        response = {
            "message": "username and password are required to register."
        }
        return response, 400
    
    username = body.get('username')
    if username is None:
        response = {
            "message": "username is required to register."
        }
        return response, 400
    
    password = body.get('password')
    if password is None:
        response = {
            "message": "password is required to register."
        }
        return response, 400
    
    existing_user = User.query.filter_by(username=username).one_or_none()
    if existing_user:
        response = {
            "message": "user already exists. please try again."
        }
        return response, 400
    
    # check to see if user entered an email and if so store it in database
    email = body.get('email')
    if email:
        user = User(email=email, username=username, password=str(password))
        user.create()
    else:
        user = User(username=username, password=str(password))
        user.create()

    response = {
        "message": "user successfully registered.",
        "data": user.to_response()
    }
    return response, 201



@auth.post('/login')
def handle_login():
    body = request.json

    if body is None:
        response = {
            "message": "username and password are required to login or email and password."
        }
        return response, 400
    
    email = body.get('email')   
    username = body.get('username')
    password = body.get('password')
    
    if password is None:
        response = {
            "message": "password is required to login."
        }
        return response, 400

    if username and email is None:
        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            response = {
                "message": "account does not exist. register or try again."
            }
            return response, 400
        
        ok = user.compare_password(password)
        if not ok:
            response = {
                "message": "invalid credentials. please try again."
            }
            return response, 401
        
        auth_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

        response = make_response({
            "message": "successfully logged in with username.",
            "token": auth_token,
            "user": user.to_response()
        })

        response.headers["Authorization"] = f"Bearer {auth_token}"
        return response, 200
    
    elif email and username is None:
        user = User.query.filter_by(email=email).one_or_none()
        if user is None:
            response = {
                "message": "account does not exist. register or try again."
            }
            return response, 400
        
        ok = user.compare_password(password)
        if not ok:
            response = {
                "message": "invalid credentials. please try again."
            }
            return response, 401
        
        auth_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        
        response = make_response({
            "message": "successfully logged in with email.",
            "token": auth_token,
            "user": user.to_response()
        })

        response.headers["Authorization"] = f"Bearer {auth_token}"
        return response, 200
    
    else:
        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            response = {
                "message": "account does not exist. register or try again."
            }
            return response, 400
        
        ok = user.compare_password(password)
        if not ok:
            response = {
                "message": "invalid credentials. please try again."
            }
            return response, 401
        
        auth_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

        response = make_response({
            "message": "successfully logged in.",
            "token": auth_token,
            "user": user.to_response()
        })

        response.headers["Authorization"] = f"Bearer {auth_token}"
        return response, 200
    


@auth.post('/editprofile')
@jwt_required()
def handle_edit_profile():
    body = request.json
    if body is None:
        response = {
            "message": "empty body - nothing was changed"
        }
        return response, 400
    
    user = User.query.filter_by(id=current_user.id).one_or_none()

    if user is None:
        response = {
            "message": "user not found"
        }
        return response, 404
    
    delete_profile = body.get('delete_profile')

    if delete_profile:
        CalorieCalculator.query.filter_by(saved_by=current_user.id).delete()
        OneRepMax.query.filter_by(saved_by=current_user.id).delete()
        FoodNutrition.query.filter_by(saved_by=current_user.id).delete()

        db.session.commit()

        user.delete()

        response = {
            "message": "user successfully deleted"
        }
        return response, 200
    
    else:
        email = body.get('email')
        username = body.get('username')
        password = body.get('password')

        if email:
            user.email = email
        if username:
            user.username = username
        if password:
            user.password = generate_password_hash(password, method='pbkdf2:sha256:260000')

        user.update()

        response = {
            "message": "Profile updated",
            "user_info": {
                "email": user.email,
                "username": user.username
            },
        }
        return response, 200