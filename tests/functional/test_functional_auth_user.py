import json
from http import HTTPStatus

def test_create_user(client, database, user):
    response = client.post("/register", json=user)

    data = json.loads(response.get_data(as_text=True))
    assert data["values"]["name"] == user["name"]

def test_create_user_twice(register):
    register(expected_status_code=HTTPStatus.OK)

    register(expected_status_code=HTTPStatus.BAD_REQUEST)


def test_create_user_with_empty_name(mock_user, register):
    user = mock_user(with_empty=['name'])

    data = register(user)

    assert data["values"]["name"] == user["name"]


def test_create_user_with_empty_email(mock_user, register):
    user = mock_user(with_empty=['email'])

    register(user, HTTPStatus.BAD_REQUEST) # Register a user that has empty email, expecting status code 400


def test_create_user_with_empty_password(mock_user, register):
    user = mock_user(with_empty=['password'])
    register(user, HTTPStatus.BAD_REQUEST) # Register a user with empty password, expecting status code 400

def test_create_user_with_empty_confirmation_password(mock_user, register):
    user = mock_user(with_empty=['confirmation_password'])
    register(user, HTTPStatus.BAD_REQUEST)


def test_create_user_without_password(mock_user, register):
    user = mock_user(without=['password'])
    register(user, HTTPStatus.BAD_REQUEST) # Register an user without password, expecting status code 400


def test_auth_user(mock_user, register, login):
    register() # Register a user with the default one, expecting status code 200

    login_user = mock_user(without=['confirmation_password'])
    data = login(login_user)

    assert data['values']['name'] == login_user['name']
    assert 'token' in data['values']

def test_auth_user_with_wrong_email(mock_user, register, login, user):
    register()

    user = mock_user(without=['name', 'confirmation_password'])
    user["email"] = "wrong_email@mail.com" # Alter the email

    login(user, HTTPStatus.BAD_REQUEST) # Login with the altered email user, expecting bad request (400)

def test_auth_user_with_wrong_password(mock_user, register, login):
    register()

    user = mock_user(without=['name','confirmation_password'])
    user["password"] = "wrongpassword"

    login(user, HTTPStatus.BAD_REQUEST)

def test_auth_user_with_empty_password(mock_user, register, login):
    register()

    user = mock_user(without=['name','confirmation_password'])
    user["password"] = ""

    login(user, HTTPStatus.BAD_REQUEST)

def test_auth_with_empty_payload(register, login):
    register()

    payload = {}
    login(payload, HTTPStatus.BAD_REQUEST)