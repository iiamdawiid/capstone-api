from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    calorie_calculator = db.relationship('CalorieCalculator', backref='user')
    onerepmax = db.relationship('OneRepMax', backref='user')
    
    def __init__(self, email, username, password):
        self.id = str(uuid4())
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def compare_password(self, password):
        return check_password_hash(self.password, password)
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'password':
                setattr(self, key, generate_password_hash(value))
            else:
                setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "date_created": self.date_created,
        }
    
class CalorieCalculator(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    gender = db.Column(db.String(6), nullable=False)
    activity_level = db.Column(db.String(30), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    units = db.Column(db.String(10), nullable=False)
    calories = db.Column(db.Integer, nullable=False)

    gain_weight1 = db.Column(db.Integer, nullable=False)
    gain_weight2 = db.Column(db.Integer, nullable=False)
    gain_weight3 = db.Column(db.Integer, nullable=False)
    lose_weight1 = db.Column(db.Integer, nullable=False)
    lose_weight2 = db.Column(db.Integer, nullable=False)
    lose_weight3 = db.Column(db.Integer, nullable=False)

    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    saved_by = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, gender, activity_level, weight, height, age, units, calories, gain_weight1, gain_weight2, gain_weight3, lose_weight1, lose_weight2, lose_weight3, saved_by):
        self.id = str(uuid4())
        self.gender = gender
        self.activity_level = activity_level
        self.weight = weight
        self.height = height
        self.age = age
        self.units = units
        self.calories = calories
        self.gain_weight1 = gain_weight1
        self.gain_weight2 = gain_weight2
        self.gain_weight3 = gain_weight3
        self.lose_weight1 = lose_weight1
        self.lose_weight2 = lose_weight2
        self.lose_weight3 = lose_weight3
        self.saved_by = saved_by

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "activity_level": self.activity_level,
            "weight": self.weight,
            "height": self.height,
            "age": self.age,
            "units": self.units,
            "calories": self.calories,
            "gain_weight1": self.gain_weight1,
            "gain_weight2": self.gain_weight2,
            "gain_weight3": self.gain_weight3,
            "lose_weight1": self.lose_weight1,
            "lose_weight2": self.lose_weight2,
            "lose_weight3": self.lose_weight3,
            "saved_at": self.saved_at,
            "saved_by": self.saved_by
        }
    
class OneRepMax(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    type_of_lift = db.Column(db.String(15), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    units = db.Column(db.String(10), nullable=False)
    one_rep_max = db.Column(db.String(50), nullable=False)

    percentage1 = db.Column(db.Integer, nullable=False)
    percentage2 = db.Column(db.Integer, nullable=False)
    percentage3 = db.Column(db.Integer, nullable=False)
    percentage4 = db.Column(db.Integer, nullable=False)
    percentage5 = db.Column(db.Integer, nullable=False)
    percentage6 = db.Column(db.Integer, nullable=False)
    percentage7 = db.Column(db.Integer, nullable=False)
    percentage8 = db.Column(db.Integer, nullable=False)

    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    saved_by = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)

    def __init__(
            self, type_of_lift, weight, reps, 
            units, one_rep_max, percentage1, percentage2, 
            percentage3, percentage4, percentage5, percentage6, 
            percentage7, percentage8, saved_by):
        
        self.id = str(uuid4())
        self.type_of_lift = type_of_lift
        self.weight = weight
        self.reps = reps
        self.units = units
        self.one_rep_max = one_rep_max
        self.percentage1 = percentage1
        self.percentage2 = percentage2
        self.percentage3 = percentage3
        self.percentage4 = percentage4
        self.percentage5 = percentage5
        self.percentage6 = percentage6
        self.percentage7 = percentage7
        self.percentage8 = percentage8
        self.saved_by = saved_by

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "type_of_lift": self.type_of_lift,
            "weight": self.weight,
            "reps": self.reps,
            "units": self.units,
            "one_rep_max": self.one_rep_max,
            "percentage1": self.percentage1,
            "percentage2": self.percentage2,
            "percentage3": self.percentage3,
            "percentage4": self.percentage4,
            "percentage5": self.percentage5,
            "percentage6": self.percentage6,
            "percentage7": self.percentage7,
            "percentage8": self.percentage8,
            "saved_at": self.saved_at,
            "saved_by": self.saved_by
        }
    
class FoodNutrition(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    food_name = db.Column(db.String, nullable=False)
    serving_size = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)

    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    saved_by = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, food_name, serving_size, calories, protein, fats, carbs, saved_by):
        self.id = str(uuid4())
        self.food_name = food_name
        self.serving_size = serving_size
        self.calories = calories
        self.protein = protein
        self.fats = fats
        self.carbs = carbs
        self.saved_by = saved_by

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "food_name": self.food_name,
            "serving_size": self.serving_size,
            "calories": self.calories,
            "protein": self.protein,
            "fats": self.fats,
            "carbs": self.carbs,
            "saved_at": self.saved_at,
            "saved_by": self.saved_by
        }