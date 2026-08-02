def test_returns_user_profile(auth_client):
    response = auth_client.get('/api/v1/profile/')
    assert response.status_code == 200
    assert response.json['name'] == 'Test User'
    assert response.json['date_of_birth'] is None
    assert response.json['sex'] is None
    assert response.json['experience_level'] is None
    assert response.json['unit_preference'] == 'metric'