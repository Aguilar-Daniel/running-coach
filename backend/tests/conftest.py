import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture 
def client(app):
    # Add a test route that only accepts GET for testing HTTP method errors
    @app.route("/api/v1/test-get-only", methods=["GET"])
    def test_get_only():
        return {"message": "OK"}, 200

    return app.test_client()


@pytest.fixture
def register_user(client): #Cannot use the default parameters in _register bc a fixture's parameters can only be other fixtures
    def _register(email="runner@example.com",
    password="password123", name="Test User"):
        response = client.post('/api/v1/auth/register', json={'email': email, 'password': password, 'name': name})
        return response
    return _register #register_user works like a lambda function in that when made an argument in another function,
    #the function calls register_user and sees what it returns and keeps that as a register_user variable 

@pytest.fixture
def auth_client(client, register_user):
    register_user()
    client.post('/api/v1/auth/login', json={'email': 'runner@example.com', 'password': 'password123'})
    csrf_token = client.get_cookie('csrf_access_token').value

    class AuthClient:
        def __init__(self, raw_client, token):
            self._client = raw_client
            self._headers = {'X-CSRF-TOKEN': token}

        def get(self, *args, **kwargs):
            return self._client.get(*args, **kwargs)    
        
        def post(self, *args, **kwargs):
            headers = {**self._headers, **kwargs.pop('headers', {})}   
            return self._client.post(*args, headers=headers, **kwargs,)  
        
        def patch(self, *args, **kwargs):
            headers = {**self._headers, **kwargs.pop('headers', {})}   
            return self._client.patch(*args, headers=headers, **kwargs)  
        
        def delete(self, *args, **kwargs):
            headers = {**self._headers, **kwargs.pop('headers', {})}   
            return self._client.delete(*args, headers=headers, **kwargs)  

    return AuthClient(client, csrf_token)    