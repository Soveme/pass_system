from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.database import get_db
from app.services.notifications import NotificationService
from app.services.calendar_integration import CalendarIntegrationService

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

@router.post("/send-test-email")
async def send_test_email(email: str, db: AsyncSession = Depends(get_db)):
    """Send test email notification"""
    result = NotificationService.send_pass_email(
        email=email,
        guest_name="Test Guest",
        qr_code="test_qr_code_12345",
        valid_until=datetime.utcnow() + timedelta(hours=8)
    )
    return {"status": "success" if result else "failed"}

@router.post("/send-test-sms")
async def send_test_sms(phone: str, db: AsyncSession = Depends(get_db)):
    """Send test SMS notification"""
    result = NotificationService.send_pass_sms(
        phone=phone,
        guest_name="Test Guest",
        qr_code="test_qr_code_12345"
    )
    return {"status": "success" if result else "failed"}

@router.get("/calendar-sync-test")
async def test_calendar_sync(db: AsyncSession = Depends(get_db)):
    """Test calendar integration"""
    google_result = CalendarIntegrationService.sync_with_google_calendar(
        user_email="test@example.com",
        event_id="event_123"
    )
    outlook_result = CalendarIntegrationService.sync_with_outlook(
        user_email="test@example.com",
        event_id="event_123"
    )
    return {
        "google_calendar": google_result,
        "outlook": outlook_result
    }
