import pytest
from mongoengine import connect, disconnect
from http import HTTPStatus

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
    def _register(custom_user=None, expected_status_code=HTTPStatus.OK):
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
    def _login(custom_user=None, expected_status_code=HTTPStatus.OK):
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


@pytest.fixture(scope="function")
def create_todo(client, database, todo, get_token):
    def _create_todo(payload=todo, expected_status_code=HTTPStatus.OK):    
        bearer_token = "Bearer {}".format(get_token())
        response = client.post('/todo', json=payload, headers={'Authorization': bearer_token })
        assert response.status_code == expected_status_code

        import json
        data = json.loads(response.get_data(as_text=True))
        return data
    return _create_todo

@pytest.fixture(scope="function")
def read_todo(client, database, get_token):
    def _read_todo(id=None, expected_status_code=HTTPStatus.OK, token=get_token()):
        path = '/todo'
        if id:
            path =f'/todo/{id}'

        bearer_token = "Bearer {}".format(token)
        response = client.get(path, headers={'Authorization': bearer_token})
        assert response.status_code == expected_status_code

        import json
        data = json.loads(response.get_data(as_text=True))
        return data

    return _read_todo


@pytest.fixture(scope="function")
def update_todo(client, database, get_token, todo):
    def _update_todo(id,todo=todo, expected_status_code=HTTPStatus.OK, token=get_token()):
        bearer_token = "Bearer {}".format(token)
        response = client.put(f'/todo/{id}', json=todo, headers={'Authorization': bearer_token})
        assert response.status_code == expected_status_code

        import json
        data = json.loads(response.get_data(as_text=True))
        return data
    return _update_todo

@pytest.fixture(scope="function")
def delete_todo(client, database, get_token, todo):
    def _delete_todo(id, expected_status_code=HTTPStatus.OK, token=get_token()):
        bearer_token = "Bearer {}".format(token)
        response = client.delete(f'/todo/{id}', headers={'Authorization':bearer_token})
        assert response.status_code == expected_status_code
    return _delete_todo