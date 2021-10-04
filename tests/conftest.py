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

@pytest.fixture
def make_user():
    def _make_user(without=[], with_empty=[]):    
        payload = {
            "name": "Edwin",
            "email": "test@mail.com",
            "password": "abcdefg",
            "confirmation_password": "abcdefg"
        }
        
        for keyword in without:
            del payload[keyword]

        for keyword in with_empty:
            payload[keyword] = ""

        return payload
    return _make_user

@pytest.fixture(scope="function")
def user(make_user):
    new_user =  make_user()
    return new_user

@pytest.fixture(scope="function")
def other_user():
    return {
        "name": "Test",
        "email": "test@mail.com",
        "password": "12345678",
        "confirmation_password": "12345678"
    }

@pytest.fixture(scope="function")
def make_todo():
    def _make_todo(without=[], with_empty=[]):
        payload= {
            "title": "Todo Payload",
            "description": "test description",
            "done": False
        }
        
        for keyword in without:
            del payload[keyword]

        for keyword in with_empty:
            payload[keyword] = ''

        return payload
    return _make_todo

@pytest.fixture(scope="function")
def todo(make_todo):
    return make_todo()

@pytest.fixture(scope="function")
def register(client, database, user):
    """
    returns a function that can be called when 
    register process is required
    """
    def _register(custom_user=None, expected_status_code=200):
        """
        By default, user already provided by fixtures above, method user()
        
        Paremeters:
        custom_user can be passed, if we want to register with customized user
        expected_status_code is for the code expected from the register process
        """
        if custom_user:
            response = client.post('/register', json=custom_user)
        else:
            response = client.post('/register', json=user)
        assert response.status_code == expected_status_code

        import json
        data = json.loads(response.get_data(as_text=True))
        return data
    return _register

@pytest.fixture(scope="function")
def login(client, database, user):
    def _login(custom_user=None, expected_status_code=200):
        if custom_user is not None:
            response = client.post('/login', json=custom_user)
        else:
            response = client.post('/login', json=user)
        assert response.status_code == expected_status_code

        import json 
        data = json.loads(response.get_data(as_text=True))
        return data
    return _login

@pytest.fixture(scope="function")
def get_token(register):
    """
    Return a user token that required for Authorization,
    this fixture already include register process, and 
    returned status code 200
    """
    def _get_token(user=None):
        data = register(user)
        return data['values']['token']['access_token']
    return _get_token
