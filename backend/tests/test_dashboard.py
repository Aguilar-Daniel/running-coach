
def test_returns_401_when_logged_out(client):
    response = client.get('/api/v1/dashboard')
    assert response.status_code == 401

def test_returns_correct_totals_and_run_count(auth_client):
    first_run = auth_client.post('/api/v1/runs', json={
        'distance_meters': 5000,
        'duration_seconds': 1400,
        'date': '2026-07-01',
    })
    assert first_run.status_code == 201
    second_run = auth_client.post('/api/v1/runs', json={
        'distance_meters': 10000,
        'duration_seconds': 2900,
        'date': '2026-07-05',
    })
    assert second_run.status_code == 201
    response = auth_client.get('/api/v1/dashboard')
    assert response.status_code == 200
    assert response.json['total_distance_meters'] == 15000
    assert response.json['run_count'] == 2

def test_new_user_has_empty_values(auth_client):
    response = auth_client.get('/api/v1/dashboard')
    assert response.status_code == 200
    assert response.json['total_distance_meters'] == 0
    assert response.json['run_count'] == 0
    assert all(pace is None for pace in response.json['average_pace_by_category'].values()) #response.json['average_pace_by_category'] is None won't work since its a dict which can't be "None"
    assert len(response.json['personal_records']) == 0

def test_run_shows_up_in_personal_records(auth_client):
    create_run = auth_client.post('/api/v1/runs', json={
        'distance_meters': 5000,
        'duration_seconds': 1400,
        'date': '2026-07-01',
    })
    assert create_run.status_code == 201
    response = auth_client.get('/api/v1/dashboard')
    assert response.status_code == 200
    pr_5k = next(r for r in response.json['personal_records'] if r['distance_category'] == '5k')
    assert pr_5k['duration_seconds'] == 1400

def test_average_pace_by_category(auth_client):
    first_5k_run = auth_client.post('/api/v1/runs', json={
        'distance_meters': 5000,
        'duration_seconds': 1400,
        'date': '2026-07-01',
    })
    assert first_5k_run.status_code == 201
    second_5k_run = auth_client.post('/api/v1/runs', json={
        'distance_meters': 5000,
        'duration_seconds': 1600,
        'date': '2026-07-01',
    })
    assert second_5k_run.status_code == 201
    first_10k_run = auth_client.post('/api/v1/runs', json={
        'distance_meters': 10000,
        'duration_seconds': 2900,
        'date': '2026-07-01',
    })
    assert first_10k_run.status_code == 201
    response = auth_client.get('/api/v1/dashboard')
    assert response.status_code == 200
    avg_5k_pace = response.json['average_pace_by_category']['5k']
    avg_10k_pace = response.json['average_pace_by_category']['10k']
    assert avg_5k_pace == 300
    assert avg_10k_pace == 290