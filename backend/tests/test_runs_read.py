def test_get_another_users_run_returns_404(auth_client, client,register_user):
        create_response = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1500,
                'date': '2026-07-01'
        })
        register_user(email='other@example.com')
        client.post('/api/v1/auth/login', json={'email': 'other@example.com', 'password': 'password123'})
        response = client.get(f"/api/v1/runs/{create_response.json['id']}")
        assert response.status_code == 404

def test_list_runs_returns_only_current_users_runs(auth_client, client, register_user):
    create_response = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1500,
                'date': '2026-07-01'
    })
    first_response = auth_client.get('/api/v1/runs')
    assert len(first_response.json['runs']) == 1
    register_user(email='other@example.com')
    client.post('/api/v1/auth/login', json={'email': 'other@example.com', 'password': 'password123'})
    second_response = client.get('/api/v1/runs')
    assert len(second_response.json['runs']) == 0

def test_get_single_run(auth_client):
    create_response = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1500,
                'date': '2026-07-01'
    })
    run_id = create_response.json['id']
    response = auth_client.get(f'/api/v1/runs/{run_id}')
    assert response.status_code == 200
    assert run_id == response.json['id']