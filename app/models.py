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
    saved_at = db.Column(db.DateTime, default = datetime.utcnow)
    saved_by = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, gender, activity_level, weight, height, age, saved_by):
        self.gender = gender
        self.activity_level = activity_level
        self.weight = weight
        self.height = height
        self.age = age
        self.saved_by = saved_by

    def create(self):
        db.session.add()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_reponse(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "activity_level": self.activity_level,
            "weight": self.weight,
            "height": self.height,
            "age": self.age,
            "saved_at": self.saved_at,
            "saved_by": self.saved_by
        }