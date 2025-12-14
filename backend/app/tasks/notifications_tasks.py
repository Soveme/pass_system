from celery import shared_task
from app.services.notifications import NotificationService
from datetime import datetime
import asyncio

@shared_task
def send_pass_email_task(email: str, guest_name: str, qr_code: str, valid_until: str):
    """Async task to send pass email"""
    valid_until_dt = datetime.fromisoformat(valid_until)
    result = NotificationService.send_pass_email(
        email=email,
        guest_name=guest_name,
        qr_code=qr_code,
        valid_until=valid_until_dt
    )
    return {"status": "sent" if result else "failed", "email": email}

@shared_task
def send_pass_sms_task(phone: str, guest_name: str, qr_code: str):
    """Async task to send pass SMS"""
    result = NotificationService.send_pass_sms(
        phone=phone,
        guest_name=guest_name,
        qr_code=qr_code
    )
    return {"status": "sent" if result else "failed", "phone": phone}

@shared_task
def send_expiration_reminder_task(email: str, guest_name: str, hours_until_expiry: int):
    """Async task to send expiration reminder"""
    result = NotificationService.send_expiration_reminder(
        email=email,
        guest_name=guest_name,
        hours_until_expiry=hours_until_expiry
    )
    return {"status": "sent" if result else "failed", "email": email}

@shared_task
def send_admin_alert_task(alert_type: str, details: dict):
    """Async task to send admin alert"""
    result = NotificationService.send_admin_alert(
        alert_type=alert_type,
        details=details
    )
    return {"status": "sent" if result else "failed", "type": alert_type}
