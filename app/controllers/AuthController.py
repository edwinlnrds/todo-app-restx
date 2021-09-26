from app.libraries.access_jwt import refresh_jwt_required
from os import access
from flask_jwt_extended.utils import create_access_token, get_jwt
from flask_restx import Resource
from flask import request
from datetime import datetime, timedelta

from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

from app.response import response
from app.transformer.UserTransformer import UserTransformer
from werkzeug.security import generate_password_hash, check_password_hash


class RegisterController(Resource):
    def post(self):
        try:
            print(request.json)
            password = request.json['password']
            confirmation_password = request.json['confirmation_password']

            if not request.json['email']:
                raise Exception('Email cannot be empty!')

            if not request.json['password']:
                raise Exception('Password cannot be empty!')

            if password != confirmation_password:
                raise Exception('Password and confirmation does not match!')

            user_exists = User.objects(email=request.json['email']).first()
            if user_exists:
                raise Exception('User already exists!')

            user = User()
            user.name = request.json['name']
            user.email = request.json['email']
            user.password = generate_password_hash(password)
            user.save()

            payload = TokenGenerator(user).generate_access_token()

            return response.ok('User registered successfully!', payload)
        except Exception as e:
            return response.bad_request('{}'.format(e), '')


class AuthController(Resource):
    def post(self):
        try:
            email = request.json['email']
            password = request.json['password']

            user = User.objects(email=email).first()

            if not user:
                raise Exception('Email or password invalid!')

            # Validate if the passwords are the same
            if not check_password_hash(user.password, password):
                raise Exception('Email or password invalid!')

            payload = TokenGenerator(user).generate_access_token()

            return response.ok(f'Welcome {user.name} with ', payload)
        except Exception as e:
            return response.bad_request('{}'.format(e), '')


class TokenGenerator(object):
    def __init__(self, user):
        self.user = user

    def generate_access_token(self):
        # generate payload token for identifier
        payload = {
            'id': str(self.user.id)
        }

        # Create access token based on payload
        access_token = create_access_token(
            identity=payload,
            fresh=True,
            expires_delta=timedelta(days=3)
        )

        # Create refresh token
        refresh_token = create_refresh_token(
            identity=payload,
            expires_delta=timedelta(days=30)
        )

        self.user = UserTransformer.single_transform(self.user)

        # Add tokens to the user object
        self.user['token'] = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return self.user


class TokenRefreshController(Resource):
    @refresh_jwt_required
    def post(self):
        try:
            token = get_jwt()

            if 'type' not in token and token['type'] != 'refresh':
                return response.unauthorized('Token is not refresh token', '')

            identity = get_jwt_identity()
            user = User.objects(id=identity['id']).first()

            if not user:
                return response.bad_request('Token is not valid', '')

            payload = TokenGenerator(user).generate_access_token()

            return response.ok(f'Token refreshed successfully', payload)
        except Exception as e:
            return response.bad_request('{}'.format(e),'')