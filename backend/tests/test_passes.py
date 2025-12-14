import pytest
from httpx import AsyncClient
from app.main import app
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_pass():
    """Test pass creation"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        now = datetime.utcnow()
        response = await ac.post(
            "/api/passes/create",
            json={
                "guest_name": "John Doe",
                "guest_company": "Tech Corp",
                "guest_phone": "+1234567890",
                "guest_email": "john@example.com",
                "valid_from": now.isoformat(),
                "valid_until": (now + timedelta(hours=8)).isoformat()
            }
        )
        assert response.status_code == 200
        assert "qr_code" in response.json()
        assert response.json()["guest_name"] == "John Doe"

@pytest.mark.asyncio
async def test_list_passes():
    """Test listing passes"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/passes/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
