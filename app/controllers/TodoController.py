from flask import Resource
from flask import request
from datetime import datetime
from app.models.todo import Todo

from app.response import response
from app.transformer.TodoTransformer import TodoTransformer

from app.libraries.access_jwt import get_identity, jwt_required

class TodoController(Resource):
    @jwt_required
    def get(self, id=None):
        user_id = get_identity()['id']
        if not id:
            # q = request.args.get('q')

            todos = Todo.objects(user_id=user_id, deleted_at=None).all()
            todos = TodoTransformer.transform(todos)
        else:
            todos = Todo.objects(id=id, user_id=user_id, deleted_at=None).first()

            if not todos:
                return response.bad_request('Todo not found!','')

            todos = TodoTransformer.single_transform(todos)

        return response.ok('', todos)

    @jwt_required
    def post(self):
        user_id = get_identity()['id']
        try:
            todo = Todo()

            if not request.json['title']:
                raise Exception("Title cannot be empty!")
        
            todo.user_id = user_id
            todo.title = request.json['title']
            todo.description = request.json['description']
            todo.save()

            return response.ok('Todo Created!', TodoTransformer.single_transform(todo))
        except Exception as e:
            return response.bad_request("{}".format(e), '')

    @jwt_required
    def put(self, id):
        try:
            todo = Todo.objects(id=id).first()

            user_id = get_identity()['id']
            if user_id != str(todo.user_id.id):
                return response.unauthorized('Unauthorized','')
            if not todo:
                return response.not_found('Todo not found', '')

            if not request.json['title']:
                raise Exception("Title cannot be empty!")

            todo.title = request.json['title']
            todo.description = request.json['description'] 
            todo.done = request.json['done']
            todo.updated_at = datetime.now()
            todo.save()

            return response.ok('Todo Updated!', TodoTransformer.single_transform(todo))
        except Exception as e:
            return response.bad_request("{}".format(e),'')

    @jwt_required
    def delete(self, id):
        try:
            todo = Todo.objects(id=id).first()

            if get_identity()['id'] != str(todo.user_id.id):
                return response.unauthorized('Unauthorized','')

            if not todo:
                return response.not_found('Todo not found!','')

            if todo.deleted_at:
                return response.bad_request('Todo does not exist!', '')
            
            todo.deleted_at = datetime.now()
            todo.save()

            return response.ok('Todo deleted successfully', TodoTransformer.single_transform(todo))
        except Exception as e:
            return response.bad_request('{e}'.format(e), '')
