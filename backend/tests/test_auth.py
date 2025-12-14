import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user import UserRole

@pytest.mark.asyncio
async def test_register():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123",
                "full_name": "Test User",
                "email": "test@example.com"
            }
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login():
    """Test user login"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First register
        await ac.post(
            "/api/auth/register",
            json={
                "username": "testuser2",
                "password": "testpass123",
                "full_name": "Test User"
            }
        )
        
        # Then login
        response = await ac.post(
            "/api/auth/login",
            json={
                "username": "testuser2",
                "password": "testpass123"
            }
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_invalid_credentials():
    """Test login with invalid credentials"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/auth/login",
            json={
                "username": "nonexistent",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401
