def test_register_creates_user_and_profile(register_user):
    response = register_user()
    assert response.status_code == 201
    assert response.json["email"] == "runner@example.com"

def test_register_rejects_duplicate_email(register_user):
    register_user()
    copy_response = register_user()
    assert copy_response.status_code == 400 
    assert "error" in copy_response.json

def test_register_rejects_short_password(client):
    response = client.post('/api/v1/auth/register', json={"email": "samplerun@example.com", "password": "short", "name": "John"})
    assert response.status_code == 400
    assert "error" in response.json

def test_login_succeeds_and_sets_cookie(client, register_user):
    access_cookie_present = False
    register_user(email='run@example.com')
    response = client.post(
        '/api/v1/auth/login',
        json={'email': 'run@example.com', "password": "password123"},
    )
    cookies = response.headers.getlist('Set-Cookie')
    for cookie in cookies:
        if 'access_token_cookie' in cookie:
            access_cookie_present = True
    assert response.status_code == 200
    assert access_cookie_present

def test_login_rejects_wrong_password(client, register_user):
    register_user()
    response = client.post('/api/v1/auth/login', json={'email': 'runner@example.com', 'password': 'wrongPassword'})
    assert response.status_code == 401
