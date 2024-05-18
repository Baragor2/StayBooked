from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("email@email.com", "password", 201),
    ("email@email.com", "password", 409),
    ("new_email@email.com", "passw0rd", 201),
    ("abcd", "password", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "hashed_password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
    ("wrong@example.com", "wrong", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "hashed_password": password,
    })

    assert response.status_code == status_code
