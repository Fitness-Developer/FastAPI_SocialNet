def test_chat_message_flow(client):
    login = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    msg = {"receiver_id":2,"content":"Hello!"}
    response = client.post("/chat/",json=msg,headers=headers)
    assert response.status_code == 200
    assert response.json()["content"] == "Hello!"