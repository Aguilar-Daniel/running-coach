from app.services.pace import calculate_pace_seconds_per_km
def test_create_run_requires_auth(client):
    response = client.post('/api/v1/runs', json={'distance_meters': 3000, 'duration_seconds': 600, 'date': '2026-07-01'})
    assert response.status_code == 401

def test_create_run_happy_path(auth_client):
    response = auth_client.post('/api/v1/runs', json={'distance_meters': 5000, 'duration_seconds': 1500, 'date': '2026-07-01'})
    assert response.status_code == 201
    assert response.json['pace_seconds_per_km'] == 300

def test_create_run_rejects_zero_distance(auth_client):
    response = auth_client.post('/api/v1/runs', json={'distance_meters': 0, 'duration_seconds': 1500, 'date': '2026-07-01'}) 
    assert response.status_code == 400

def test_create_run_rejects_invalid_perceived_effort(auth_client):
    response = auth_client.post('/api/v1/runs', json={'distance_meters': 5000, 'duration_seconds': 1500, 'date': '2026-07-01', 'perceived_effort': 'extremely difficult'})
    assert response.status_code == 400