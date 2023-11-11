from flask import Flask
app = Flask(__name__)

from config import Config
app.config.from_object(Config)

from .models import db, User
db.init_app(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

from flask_jwt_extended import JWTManager
jwt = JWTManager(app)

from flask_cors import CORS
CORS(app, supports_credentials=True)

@jwt.user_identity_loader
def user_identity_lookup(id):
    return id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).one_or_none()

from .auth import auth_blueprint
app.register_blueprint(auth_blueprint)

from .calorie_calculator import calorie_calculator_blueprint
app.register_blueprint(calorie_calculator_blueprint)

from .onerepmax import onerepmax_blueprint
app.register_blueprint(onerepmax_blueprint)