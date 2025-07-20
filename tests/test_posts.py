def test_create_posts(client):
    login = client.post("/auth/login",data={"username": "testuser","password":"testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    post_data = {"title":"Armwrestling","content":"Levan №1"}
    response = client.post("/posts/",json=post_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Armwrestling"


