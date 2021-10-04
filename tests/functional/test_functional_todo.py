import json
from http import HTTPStatus


def test_create_todo(todo, create_todo):
    data = create_todo()
    assert data['values']['title'] == todo['title']
    assert data['values']['done'] == False


def test_create_todo_with_empty_title(mock_todo, create_todo):
    todo = mock_todo(with_empty=['title'])
    create_todo(todo, HTTPStatus.BAD_REQUEST)

def test_create_todo_with_empty_description(mock_todo, create_todo):
    todo = mock_todo(with_empty=['description'])
    data = create_todo(todo)

    assert data['values']['title'] == todo['title']
    assert data['values']['description'] == todo['description']
    assert data['values']['done'] == todo['done']

def test_create_todo_without_description(mock_todo, create_todo):
    todo = mock_todo(without=['description'])
    create_todo(todo, HTTPStatus.BAD_REQUEST)


def test_create_todo_without_headers(client, database, todo):
    response = client.post('/todo', json=todo)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_create_todo_without_token(client, database, todo):
    token = ""
    response = client.post('/todo', json=todo, headers={'Authorization': token})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_read_todo(create_todo, read_todo):
    data = create_todo()
    id = data['values']['id']

    read_data = read_todo(id)

    assert data['values']['title'] == read_data['values']['title']
    assert data['values']['description'] == read_data['values']['description']
    assert data['values']['done'] == False


def test_read_todos(mock_todo, get_token, create_todo, read_todo):
    payload = [
        mock_todo(title="Todo 1", description="Todo 1 description"),
        mock_todo(title="Todo 2", description="Todo 2 description"),
        mock_todo(title="Todo 3", description="Todo 3 description")
    ]

    token = get_token()
    for item in payload:
        create_todo(item, token=token)

    data = read_todo()

    for index in range(len(payload)):
        item = data['values']
        assert item[index]["title"] == payload[index]["title"]
        assert item[index]["description"] == payload[index]["description"]


def test_read_todo_with_wrong_id(create_todo, read_todo):
    create_todo()
    id = '615af37e76d592047555c27z'
    read_todo(id, HTTPStatus.BAD_REQUEST)


def test_update_todo(mock_todo, create_todo, update_todo):
    id = create_todo()['values']['id']
    
    new_data = mock_todo(title="New Todo")

    result = update_todo(id=id, todo=new_data)

    assert result['values']['title'] == new_data['title']
    assert result['values']['description'] == new_data['description']
    assert result['values']['done'] == False


def test_update_todo_done_status(mock_todo, create_todo, update_todo):
    data = create_todo()
    id = data['values']['id']

    payload = mock_todo(done=True)
    data = update_todo(id, todo=payload)
    assert data['values']['done'] == True


def test_update_todo_with_empty_description(mock_todo, create_todo, update_todo):
    data = create_todo()
    id = data['values']['id']
    
    payload = mock_todo(with_empty=['description'])
    data = update_todo(id, todo=payload)
    assert data['values']['title'] == payload['title']
    assert data['values']['description'] == payload['description']
    assert data['values']['done'] == payload['done']


def test_update_todo_empty_title(mock_todo, create_todo, update_todo):
    data = create_todo()
    id = data['values']['id']

    payload = mock_todo(with_empty=['title'])
    update_todo(id, payload, HTTPStatus.BAD_REQUEST)


def test_update_todo_without_title(mock_todo, create_todo, update_todo):
    data = create_todo()
    id = data['values']['id']

    payload = mock_todo(without=['title'])
    update_todo(id, payload, HTTPStatus.BAD_REQUEST)


def test_update_without_description(mock_todo, create_todo, update_todo):
    data = create_todo()
    id = data['values']['id']
    
    payload = mock_todo(without=['description'])
    update_todo(id, payload, HTTPStatus.BAD_REQUEST)


def test_update_without_done_status(mock_todo, create_todo, update_todo):
    data = create_todo()
    id = data['values']['id']

    payload = mock_todo(without=['done'])
    update_todo(id, payload, HTTPStatus.BAD_REQUEST)


def test_update_todo_with_different_user(mock_todo, create_todo, update_todo, get_token, other_user):
    data = create_todo()
    id = data['values']['id']

    token = get_token(other_user)

    payload = mock_todo(description="Test update by other user",done=True)
    update_todo(id, payload, HTTPStatus.UNAUTHORIZED, token)


def test_update_todo_with_wrong_id(mock_todo, create_todo, update_todo):
    data = create_todo()
    id = id = 'a' + data['values']['id'][1:len(data['values']['id'])]

    payload = mock_todo(description="test update with wrong id", done=True)
    update_todo(id, payload, HTTPStatus.NOT_FOUND)


def test_delete_todo(create_todo, delete_todo):
    data = create_todo()
    id = data['values']['id']
    delete_todo(id)


def test_delete_todo_with_different_user(create_todo, delete_todo, get_token, other_user):
    data = create_todo()
    id = data['values']['id']
    
    other_token = get_token(other_user)
    delete_todo(id, HTTPStatus.UNAUTHORIZED, other_token)


def test_delete_todo_with_wrong_id(create_todo, delete_todo):
    create_todo()
    id = '6153377b3eb3c495ef888888'  # random id
    delete_todo(id, HTTPStatus.NOT_FOUND)

def test_delete_todo_twice(create_todo, delete_todo):
    data = create_todo()
    id = data['values']['id']

    delete_todo(id)
    delete_todo(id, HTTPStatus.BAD_REQUEST)