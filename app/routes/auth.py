from flask import Blueprint
from flask_restx import Api
from app.controllers.AuthController import RegisterController, AuthController, TokenRefreshController

auth_blueprint = Blueprint('auth', __name__)
auth = Api(auth_blueprint)

# Register route
auth.add_resource(RegisterController, '/register')
# Login route
auth.add_resource(AuthController, '/login')
# Refresh token
auth.add_resource(TokenRefreshController, '/refresh')