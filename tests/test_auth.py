def test_register_and_login(client):
    data = {"username": "testuser", "email": "test@example.com", "password": "testpass"}

    response = client.post("/auth/register", json=data)
    print("Register response:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    login_data = {"username": "testuser", "password": "testpass"}
    login_response = client.post("/auth/login", data=login_data)
    print("Login response:", login_response.status_code, login_response.json())
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()