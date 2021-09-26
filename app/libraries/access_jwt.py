from functools import wraps

from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.utils import get_jwt_identity
from app.response import response

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return response.unauthorized('Unauthorized','')
        return fn(*args, **kwargs)
    return wrapper

# wrap a function to verify JWT
def refresh_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(refresh=True)
        except Exception as e:
            return response.unauthorized('Unauthorized','')
        return fn(*args, **kwargs)
    return wrapper

def get_identity():
    return get_jwt_identity()