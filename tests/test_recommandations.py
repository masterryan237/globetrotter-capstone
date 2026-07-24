def test_recommendations(client):

    response = client.get(
        "/recommendations",
        headers={
            "Authorization": "Bearer fake_token"
        }
    )


    assert response.status_code in [200,401]