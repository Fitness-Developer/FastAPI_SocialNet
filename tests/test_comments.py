def test_create_comment(client):
    login = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    comment_data = {"content":"Cool post!","post_id": 1}
    response = client.post("/comments/",json=comment_data,headers=headers)
    assert response.status_code == 200
    assert response.json()["content"] == "Cool post!"