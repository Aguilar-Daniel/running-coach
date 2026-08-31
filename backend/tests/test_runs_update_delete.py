def test_update_run_happy_path(auth_client):
    create_response = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1500,
                'date': '2026-07-01'
    })
    run_id = create_response.json['id']
    patch_response = auth_client.patch(f'/api/v1/runs/{run_id}', json={'notes': 'easy run'})
    assert patch_response.status_code == 200
    get_response = auth_client.get(f'/api/v1/runs/{run_id}')
    assert get_response.json['notes'] == 'easy run'

def test_update_another_users_run_returns_404(auth_client, client, register_user): 
    create_response = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1500,
                'date': '2026-07-01'
    })
    run_id = create_response.json['id']
    register_user(email='other@example.com')
    login_request = client.post('/api/v1/auth/login', json={'email': 'other@example.com', 'password': 'password123'}) 
    csrf_token = client.get_cookie('csrf_access_token').value
    patch_response = client.patch(f'/api/v1/runs/{run_id}', json={'notes': 'fake note'}, headers={'X-CSRF-TOKEN': csrf_token})
    assert patch_response.status_code == 404

def test_delete_run_then_get_returns_404(auth_client): 
    create_response = auth_client.post('/api/v1/runs', json={
                'distance_meters': 5000,
                'duration_seconds': 1500,
                'date': '2026-07-01'
    })
    run_id = create_response.json['id']
    delete_response = auth_client.delete(f'/api/v1/runs/{run_id}')
    assert delete_response.status_code == 204
    get_response = auth_client.get(f'/api/v1/runs/{run_id}')
    assert get_response.status_code == 404
