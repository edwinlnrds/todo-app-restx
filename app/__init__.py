from flask import Flask
from app.config import Config
app = Flask(__name__)
app.config.from_object(Config)

# Initiate api 
from flask_restx import Api
api = Api(app)

from flask_jwt_extended import JWTManager
jwt = JWTManager(app)

from app.db_manager import DatabaseManager
DatabaseManager.open_database()

from app import routes