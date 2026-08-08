def test_returns_user_profile(auth_client):
    response = auth_client.get('/api/v1/profile/')
    assert response.status_code == 200
    assert response.json['name'] == 'Test User'
    assert response.json['date_of_birth'] is None
    assert response.json['sex'] is None
    assert response.json['experience_level'] is None
    assert response.json['unit_preference'] == 'metric'

def test_updates_profile_fields(auth_client):
    response = auth_client.patch('/api/v1/profile/', json={'name': 'New Name', 'sex': 'male', 'unit_preference': 'imperial'})
    assert response.status_code == 200
    assert response.json['name'] == 'New Name'
    assert response.json['sex'] == 'male'   
    assert response.json['unit_preference'] == 'imperial'

def test_catches_fake_fields(auth_client):
    response = auth_client.patch('/api/v1/profile/', json={'name': 'New Name', 'not_a_real_field': 'x'})
    assert response.status_code == 400