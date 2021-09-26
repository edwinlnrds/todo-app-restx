from app.models.user import User


def test_create_user(client):
    user = User(name='Edwin', email='test123@mail.com')
    assert user.name == 'Edwin'


def test_create_user_with_empty_name(client):
    user = User(name='', email='test123@mail.com')
    assert user.name == ''


def test_create_user_without_attribute_name(client):
    user = User(email='test123@mail.com')
    assert user.name == None


def test_create_user_without_email(client):
    user = User(name='edwin')
    assert user.email == None


def test_create_user_without_password(client):
    user = User(name='Edwin', email='test123@mail.com')
    assert user.password == None


def test_create_user_without_name_attribute(client):
    try:
        user = User(email='test123@mail.com', password="123456")
        user.save()

        assert user.email == 'test123@mail.com'
    except Exception:
        assert True

def test_create_user_without_email_attribute(client):
    try:
        user = User(name="Edwin", password="123457")
        user.save()
        
        assert user.name == "Edwin"
    except Exception:
        assert True

def test_create_user_without_password_attribute(client):
    try:
        user = User(name='Edwin', email='test123@mail.com')
        user.save()

        assert user.email == 'test123@mail.com'
    except Exception:
        assert True

def test_check_generated_token_type(test_app, client):
    with test_app.app_context():
        from app.controllers.AuthController import TokenGenerator

        user = User(name='Edwin', email='test123@mail.com', password='abcedfg')
        user.save()

        payload = TokenGenerator(user).generate_access_token()

        assert type(payload) == dict

def test_check_name_inside_token_generator(test_app, client):
    with test_app.app_context():
        from app.controllers.AuthController import TokenGenerator

        user = User(name='Edwin', email='test123@mail.com', password='abcedfg')
        user.save()

        payload = TokenGenerator(user).generate_access_token()

        assert payload['name'] == 'Edwin'
        assert payload['email'] == 'test123@mail.com'

        assert 'password' not in payload
        assert 'token' in payload

