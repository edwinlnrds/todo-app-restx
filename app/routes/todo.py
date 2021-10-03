from flask import Blueprint
from flask_restx import Api
from app.controllers.TodoController import TodoController

todo_blueprint = Blueprint('todo', __name__)
todo = Api(todo_blueprint)

# Todo Routes
todo.add_resource(TodoController,'/todo', '/todo/<string:id>')
