def test_register(client):
    response = client.post(
        "/register",
        json={
            "username": "alice",
            "password": "s3cr3t",
            "preferences": ["beach", "food"]
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["username"] == "alice"

def test_login(client):

    response = client.post(
        "/login",
        json={
            "username":"alice",
            "password":"s3cr3t"
        }
    )


    assert response.status_code == 200

    data = response.get_json()

    assert "token" in data