import json

def test_create_user(client, database, user):
    response = client.post("/register", json=user)

    data = json.loads(response.get_data(as_text=True))
    assert data["values"]["name"] == user["name"]

def test_create_user_twice(client, database, user):
    response = client.post("/register", json=user)
    assert response.status_code == 200

    response = client.post("/register", json=user)
    assert response.status_code == 400


def test_create_user_with_empty_name(client, database, user):
    user["name"] = ""

    response = client.post("/register", json=user)
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["values"]["name"] == ""


def test_create_user_with_empty_email(client, database, user):
    user["email"] = ""

    response = client.post("/register", json=user)
    assert response.status_code == 400


def test_create_user_with_empty_password(client, database, user):
    user["password"] = ""

    response = client.post("/register", json=user)
    assert response.status_code == 400


def test_create_user_with_empty_confirmation_password(client, database, user):
    user["confirmation_password"] = ""

    response = client.post("/register", json=user)
    assert response.status_code == 400


def test_create_user_without_password(client, database, user):
    del user["password"]
    response = client.post('/register', json=user)
    assert response.status_code == 400


def test_auth_user(client, database, user):
    client.post('/register', json=user)

    name = user["name"]
    del user["name"]
    del user["confirmation_password"]

    response = client.post('/login', json=user)
    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['name'] == name
    assert 'token' in data['values']

def test_auth_user_with_wrong_email(client, database, user):
    client.post('/register', json=user)

    del user["name"]
    del user["confirmation_password"]
    user["email"] = "wrong_email@mail.com"

    response = client.post('/login', json=user)
    assert response.status_code == 400

def test_auth_user_with_wrong_password(client, database, user):
    client.post('/register', json=user)

    user["password"] = "wrongpassword"

    response = client.post('/login', json=user)
    assert response.status_code == 400


def test_auth_user_with_empty_password(client, database, user):
    client.post('/register', json=user)

    del user["name"]
    del user["confirmation_password"]
    user["password"] = ""

    response = client.post('/login', json=user)
    assert response.status_code == 400

def test_auth_with_empty_payload(client, database, user):
    client.post('/register', json=user)

    payload = {}
    response = client.post('/login', json=payload)
    assert response.status_code == 400