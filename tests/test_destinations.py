def test_destinations(client):

    response = client.get(
        "/destinations?tag=beach&max_cost=100"
    )


    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)