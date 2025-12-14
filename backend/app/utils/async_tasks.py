from app.celery_app import app as celery_app
from app.tasks.notifications_tasks import (
    send_pass_email_task,
    send_pass_sms_task,
    send_expiration_reminder_task,
    send_admin_alert_task
)
from datetime import datetime

class AsyncTaskRunner:
    """Wrapper for Celery tasks"""
    
    @staticmethod
    def send_pass_email(email: str, guest_name: str, qr_code: str, valid_until: datetime):
        """Queue email sending task"""
        send_pass_email_task.delay(
            email=email,
            guest_name=guest_name,
            qr_code=qr_code,
            valid_until=valid_until.isoformat()
        )
    
    @staticmethod
    def send_pass_sms(phone: str, guest_name: str, qr_code: str):
        """Queue SMS sending task"""
        send_pass_sms_task.delay(
            phone=phone,
            guest_name=guest_name,
            qr_code=qr_code
        )
    
    @staticmethod
    def send_expiration_reminder(email: str, guest_name: str, hours_until_expiry: int):
        """Queue expiration reminder task"""
        send_expiration_reminder_task.delay(
            email=email,
            guest_name=guest_name,
            hours_until_expiry=hours_until_expiry
        )
    
    @staticmethod
    def send_admin_alert(alert_type: str, details: dict):
        """Queue admin alert task"""
        send_admin_alert_task.delay(
            alert_type=alert_type,
            details=details
        )
