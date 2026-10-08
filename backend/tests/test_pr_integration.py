from app.services.pr_matching import match_distance_category

def test_pr_creation(auth_client):
    create_response = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1200,
                'date': '2026-07-01'
    })
    assert create_response.status_code == 201
    records = auth_client.get('/api/v1/records')
    pr_5k = next(r for r in records.json['records'] if r['distance_category'] == '5k') # makes the pr_5k variable the first run with a distance cat of 5k
    assert pr_5k['duration_seconds'] == 1200

def test_pr_update(auth_client): 
    slow_run = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1400,
                'date': '2026-07-01'
    }) 
    assert slow_run.status_code == 201
    pr_run = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1100,
                'date': '2026-07-01'
    })
    assert pr_run.status_code == 201
    records = auth_client.get('/api/v1/records')
    assert records.status_code == 200
    pr_5k = next(r for r in records.json['records'] if r['distance_category'] == '5k')
    assert pr_5k['duration_seconds'] == 1100

def test_pr_persists(auth_client):
    fast_run = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1100,
                'date': '2026-07-01'
    }) 
    assert fast_run.status_code == 201
    slow_run = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1400,
                'date': '2026-07-01'
    })
    assert slow_run.status_code == 201
    records = auth_client.get('/api/v1/records')
    assert records.status_code == 200
    pr_5k = next(r for r in records.json['records'] if r['distance_category'] == '5k')
    assert pr_5k['duration_seconds'] == 1100    

def test_delete_run_updates_pr(auth_client):
    slow_run = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1400,
                'date': '2026-07-01'
    }) 
    assert slow_run.status_code == 201
    pr_run = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1100,
                'date': '2026-07-01'
    })    
    assert pr_run.status_code == 201
    delete_request = auth_client.delete(f"/api/v1/runs/{pr_run.json['id']}")
    assert delete_request.status_code == 204
    records = auth_client.get('/api/v1/records')
    assert records.status_code == 200
    pr_5k = next(r for r in records.json['records'] if r['distance_category'] == '5k')
    assert pr_5k['duration_seconds'] == 1400 