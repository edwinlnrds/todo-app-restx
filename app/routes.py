from app import api
from app.controllers import AuthController, TodoController

# Register route
api.add_resource(AuthController.RegisterController, '/register')
# Login route
api.add_resource(AuthController.AuthController, '/login')
# Refresh token
api.add_resource(AuthController.TokenRefreshController, '/refresh')
# Todo Routes
api.add_resource(TodoController.TodoController,'/todo', '/todo/<string:id>')
