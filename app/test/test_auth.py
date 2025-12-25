def test_register_and_login(client):
    # Register
    res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@test.com",
            "password": "123",
        },
    )
    assert res.status_code == 201
    assert "id" in res.json()

    # Login
    res = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@test.com",
            "password": "123",
        },
    )
    assert res.status_code == 200

    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
