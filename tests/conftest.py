import pytest
from mongoengine import connect, disconnect

@pytest.fixture
def test_app():
    from app import create_app
    from app.config import TestingConfig
    app = create_app(TestingConfig)
    return app

@pytest.fixture
def client(test_app):
    return test_app.test_client()
    
@pytest.fixture(scope="function")
def database(test_app):
    with test_app.app_context():
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost/mocking_db')

@pytest.fixture(scope="function")
def user():
    payload = {
        "name": "Edwin",
        "email": "test@mail.com",
        "password": "abcdefg",
        "confirmation_password": "abcdefg"
    }
    
    return payload

@pytest.fixture(scope="function")
def other_user():
    return {
        "name": "Test",
        "email": "test@mail.com",
        "password": "12345678",
        "confirmation_password": "12345678"
    }