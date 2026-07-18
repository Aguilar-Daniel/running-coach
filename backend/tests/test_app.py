def test_unknown_route_returns_json_404(client):
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    assert response.json["error"]


def test_wrong_method_returns_json_405(client):
    """Test that POST to a GET-only route returns JSON 405, not HTML."""
    response = client.post("/api/v1/test-get-only")
    assert response.status_code == 405
    assert response.content_type == "application/json"
    assert "error" in response.json
