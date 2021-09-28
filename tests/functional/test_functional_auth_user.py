import json

def test_create_user(client, database):
    payload = {
        "name": "Edwin",
        "email": "test@mail.com",
        "password": "abcdefg",
        "confirmation_password": "abcdefg"
    }

    response = client.post("/register", json=payload)

    data = json.loads(response.get_data(as_text=True))
    assert data["values"]["name"] == "Edwin"

def test_create_user_twice(client, database):
    payload = {
        "name": "Edwin",
        "email": "test@mail.com",
        "password": "abcdefg",
        "confirmation_password": "abcdefg"
    }

    response = client.post("/register", json=payload)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200

    response = client.post("/register", json=payload)
    assert response.status_code == 400


def test_create_user_with_empty_name(client, database):
    payload = {
        "name": "",
        "email": "test@mail.com",
        "password": "abcdefg",
        "confirmation_password": "abcdefg"
    }

    response = client.post("/register", json=payload)

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["values"]["name"] == ""


def test_create_user_with_empty_email(client, database):
    payload = {
        "name": "Edwin",
        "email": "",
        "password": "abcdefg",
        "confirmation_password": "abcdefg"
    }

    response = client.post("/register", json=payload)
    assert response.status_code == 400


def test_create_user_with_empty_password(client, database):
    payload = {
        "name": "Edwin",
        "email": "test@mail.com",
        "password": "",
        "confirmation_password": "abcdefg"
    }

    response = client.post("/register", json=payload)
    assert response.status_code == 400


def test_create_user_with_empty_confirmation_password(client, database):
    payload = {
        "name": "Edwin",
        "email": "test@mail.com",
        "password": "abcdefg",
        "confirmation_password": ""
    }

    response = client.post("/register", json=payload)
    assert response.status_code == 400


def test_create_user_without_password(client, database):
    payload = {
        "name": "User",
        "email": "user@mail.com",
        "confirmation_password": "abcdefgh"
    }
    response = client.post('/register', json=payload)
    assert response.status_code == 400


def test_auth_user(client, database):
    payload = {
        "name": "Test",
        "email": "test@mail.com",
        "password": "12345678",
        "confirmation_password": "12345678",
    }
    client.post('/register', json=payload)

    payload = {
        "email": "test@mail.com",
        "password": "12345678",
    }
    response = client.post('/login', json=payload)
    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['name'] == "Test"
    assert 'token' in data['values']

def test_auth_user_with_wrong_email(client, database):
    payload = {
        "name": "Test",
        "email": "test@mail.com",
        "password": "12345678",
        "confirmation_password": "12345678",
    }
    client.post('/register', json=payload)

    payload = {
        "email": "wrong.email@mail.com",
        "password": "12345678",
    }
    response = client.post('/login', json=payload)
    assert response.status_code == 400

def test_auth_user_with_wrong_password(client, database):
    payload = {
        "name": "Test",
        "email": "test@mail.com",
        "password": "12345678",
        "confirmation_password": "12345678",
    }
    client.post('/register', json=payload)

    payload = {
        "email": "test@mail.com",
        "password": "12345678910"
    }

    response = client.post('/login', json=payload)
    assert response.status_code == 400


def test_auth_user_with_empty_password(client, database):
    payload = {
        "name": "Test",
        "email": "test@mail.com",
        "password": "12345678",
        "confirmation_password": "12345678"
    }
    client.post('/register', json=payload)

    payload = {
        "email": "test@mail.com",
        "password": ""
    }
    response = client.post('/login', json=payload)
    assert response.status_code == 400

def test_auth_with_empty_payload(client, database):
    payload = {
        "name": "Test",
        "email": "test@mail.com",
        "password": "12345678",
        "confirmation_password": "12345678"
    }
    client.post('/register', json=payload)

    payload = {}
    response = client.post('/login', json=payload)
    assert response.status_code == 400