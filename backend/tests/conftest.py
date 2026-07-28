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