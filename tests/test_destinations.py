def test_destinations(client):

    response = client.get(
        "/destinations?tag=beach&max_cost=100"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "destinations" in data
    assert isinstance(data["destinations"], list)
    assert data["count"] > 0