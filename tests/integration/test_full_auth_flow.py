import pytest


@pytest.mark.asyncio
async def test_full_auth_flow(client):

    response = await client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123456"
    })
    assert response.status_code == 201

    response = await client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "123456"
    })
    assert response.status_code == 200

    body = response.json()
    access_token = body["access_token"]

    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200