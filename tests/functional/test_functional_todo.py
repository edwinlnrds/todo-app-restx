import json

def test_create_todo(client, database):
    payload = {
        "name": "John Doe",
        "email": "johndoe@mail.com",
        "password": "123456",
        "confirmation_password": "123456"
    }
    response = client.post('/register', json=payload)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Minum Air",
        "description": "Minum air 1 Liter"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    data = json.loads(response.get_data(as_text=True))
    assert data['values']['title'] == "Minum Air"
    assert data['values']['done'] == False


def test_create_todo_with_empty_title(client, database):
    payload = {
        "name": "John Doe",
        "email": "johndoe@mail.com",
        "password": "123456",
        "confirmation_password": "123456"
    }
    response = client.post('/register', json=payload)
    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "",
        "description": "Nothing here."
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400


def test_create_todo_without_description(client, database):
    payload = {
        "name": "John Doe",
        "email": "johndoe@mail.com",
        "password": "123456",
        "confirmation_password": "123456"
    }
    response = client.post('/register', json=payload)
    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Todo without description",
        "description": ""
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['values']['title'] == "Todo without description"
    assert data['values']['description'] == ""
    assert data['values']['done'] == False


def test_create_todo_without_headers(client, database):
    payload = {
        "title": "Todo without headers",
        "description": ""
    }
    response = client.post('/todo', json=payload)

    assert response.status_code == 401


def test_create_todo_without_token(client, database):
    payload = {
        "title": "Todo without token",
        "description": "Should return 401/Unauthorized"
    }
    token = ""
    response = client.post('/todo', json=payload, headers={'Authorization': token})

    assert response.status_code == 401

def test_read_todo(client, database):
    payload = {
        "name": "John Doe",
        "email": "johndoe@mail.com",
        "password": "123456",
        "confirmation_password": "123456"
    }
    response = client.post('/register', json=payload)
    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Todo test",
        "description": "Here lies the description"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    
    id = data['values']['id']

    response = client.get(f'/todo/{id}', headers={'Authorization': token})
    data = json.loads(response.get_data(as_text=True))

    assert data['values']['title'] == payload['title']
    assert data['values']['description'] == payload['description']
    assert data['values']['done'] == False

def test_read_todo_without_id(client, database):
    pass

def test_read_todo_without_token(client, database):
    pass

def test_read_todo_not_found(client, database):
    pass

def test_read_todo_by_another_user(client, database):
    pass

def test_update_todo(client, database):
    payload = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=payload)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing dish!",
        "description":"Washing dish leftfover from the party yesterday."
    }
    response = client.post('/todo', json=payload, headers= {'Authorization':token})

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['title'] == "Washing dish!"
    assert data['values']['description'] == "Washing dish leftfover from the party yesterday."
    assert data['values']['done'] == False

def test_update_todo_done_status(client, database):
    payload = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=payload)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing dish!",
        "description":"Washing dish leftfover from the party yesterday."
    }
    response = client.post('/todo', json=payload, headers= {'Authorization':token})
    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['title'] == "Washing dish!"
    assert data['values']['description'] == "Washing dish leftfover from the party yesterday."
    assert data['values']['done'] == False

    id = data['values']['id']

    payload = {
        "title":"test",
        "description":"boo",
        "done": True
    }
    response = client.put(f'/todo/{id}', json=payload, headers={'Authorization':token})
    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['done'] == True


def test_update_todo_with_empty_description(client, database):
    payload = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=payload)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing dish!",
        "description":"lalalala"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['title'] == payload['title']
    assert data['values']['done'] == False

    id = data['values']['id']

    payload = {
        "title":"REEEEEEEE",
        "description": "",
        "done": False
    }
    response = client.put(f'/todo/{id}', json=payload, headers={'Authorization': token})
    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['title'] == payload['title']
    assert data['values']['description'] == payload['description']
    assert data['values']['done'] == payload['done']


def test_update_todo_empty_title(client, database):
    payload = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=payload)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing car!",
        "description":"lalalala"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['title'] == payload['title']
    assert data['values']['done'] == False

    id = data['values']['id']

    payload = {
        "title":"",
        "description":"payload without title",
        "done":False
    }
    response = client.put(f'/todo/{id}', json=payload, headers = {'Authorization': token})
    assert response.status_code == 400


def test_update_todo_without_title(client, database):
    payload = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=payload)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Sleep!",
        "description":"lalalala"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data['values']['title'] == payload['title']
    assert data['values']['done'] == False

    id = data['values']['id']

    payload = {
        "description":"Without title in the dict!",
        "done": False
    }
    response = client.put(f'/todo/{id}', json=payload, headers={'Authorization': token})
    assert response.status_code == 400

def test_update_without_description(client, database):
    payload = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=payload)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing car!",
        "description":"lalalala"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    assert response.status_code == 200
    
    id = data['values']['id']

    payload = {
        "title": "Todo without description",
        "done": False
    }
    response = client.put(f'/todo/{id}', json=payload, headers={'Authorization': token})
    assert response.status_code == 400

def test_update_without_done_status(client, database):
    payload = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=payload)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing car!",
        "description":"lalalala"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    assert response.status_code == 200
    
    id = data['values']['id']

    payload = {
        "title": "Todo",
        "description":"without done status."
    }
    response = client.put(f'/todo/{id}', json=payload, headers={'Authorization': token})
    assert response.status_code == 400

def test_update_todo_with_different_user(client, database):
    owner = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=owner)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing car!",
        "description":"lalalala"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))

    id = data['values']['id']

    another_user = {
        "name": "Booze",
        "email": "booze@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=another_user)
    data = json.loads(response.get_data(as_text=True))

    other_token = "Bearer {}".format(data['values']['token']['access_token'])
    
    payload = {
        "title": "Todo",
        "description":"test update by another user.",
        "done": True
    }
    response = client.put(f'/todo/{id}', json=payload, headers={'Authorization': other_token})
    assert response.status_code == 401

def test_delete_todo(client, database):
    owner = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=owner)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing car!",
        "description":"lalalala"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))

    id = data['values']['id']

    response = client.delete(f'/todo/{id}', headers={'Authorization': token})
    assert response.status_code == 200

def test_delete_todo_with_different_user(client, database):
    owner = {
        "name": "Edwin",
        "email": "sample@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=owner)

    data = json.loads(response.get_data(as_text=True))
    token = "Bearer {}".format(data['values']['token']['access_token'])

    payload = {
        "title": "Washing car!",
        "description":"lalalala"
    }
    response = client.post('/todo', json=payload, headers={'Authorization': token})
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))

    id = data['values']['id']

    another_user = {
        "name": "Booze",
        "email": "booze@mail.com",
        "password": "thisisapassword",
        "confirmation_password": "thisisapassword"
    }
    response = client.post('/register', json=another_user)
    data = json.loads(response.get_data(as_text=True))

    other_token = "Bearer {}".format(data['values']['token']['access_token'])

    response = client.delete(f'/todo/{id}', headers={'Authorization': other_token})
    assert response.status_code == 401