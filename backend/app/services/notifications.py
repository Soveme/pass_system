import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from datetime import datetime
import json

class NotificationService:
    """Send email and SMS notifications"""
    
    @staticmethod
    def send_pass_email(email: str, guest_name: str, qr_code: str, valid_until: datetime):
        """
        Send pass details via email (STUB)
        In production, integrate with SendGrid, Mailgun, or AWS SES
        """
        try:
            subject = f"Your Access Pass - Pass System"
            body = f"""
            Hello {guest_name},
            
            Your access pass has been successfully created!
            
            Pass Details:
            - Valid until: {valid_until.strftime('%d.%m.%Y %H:%M')}
            - QR Code: {qr_code}
            
            Show the QR code to the guard at the entrance.
            
            Best regards,
            Pass System Team
            """
            
            print(f"[EMAIL_STUB] Sending email to {email}")
            print(f"[EMAIL_STUB] Subject: {subject}")
            print(f"[EMAIL_STUB] Body:\n{body}")
            
            # In production:
            # msg = MIMEMultipart()
            # msg['From'] = settings.smtp_user
            # msg['To'] = email
            # msg['Subject'] = subject
            # msg.attach(MIMEText(body, 'plain'))
            # 
            # server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
            # server.starttls()
            # server.login(settings.smtp_user, settings.smtp_password)
            # server.send_message(msg)
            # server.quit()
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            return False
    
    @staticmethod
    def send_pass_sms(phone: str, guest_name: str, qr_code: str):
        """
        Send pass QR code via SMS (STUB)
        In production, integrate with Twilio or AWS SNS
        """
        try:
            message = f"Pass System: Your access pass QR code: {qr_code[:20]}... Valid for 8 hours."
            
            print(f"[SMS_STUB] Sending SMS to {phone}")
            print(f"[SMS_STUB] Message: {message}")
            
            # In production:
            # from twilio.rest import Client
            # client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            # message = client.messages.create(
            #     body=message,
            #     from_=settings.twilio_phone_number,
            #     to=phone
            # )
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send SMS: {e}")
            return False
    
    @staticmethod
    def send_expiration_reminder(email: str, guest_name: str, hours_until_expiry: int):
        """
        Send expiration reminder email
        """
        print(f"[EMAIL_STUB] Sending expiration reminder to {email}")
        print(f"[EMAIL_STUB] Guest {guest_name}'s pass expires in {hours_until_expiry} hours")
        return True
    
    @staticmethod
    def send_guard_notification(title: str, message: str, guard_id: int = None):
        """
        Send push notification to guard
        """
        print(f"[PUSH_NOTIFICATION] Title: {title}")
        print(f"[PUSH_NOTIFICATION] Message: {message}")
        if guard_id:
            print(f"[PUSH_NOTIFICATION] Target Guard ID: {guard_id}")
        return True
    
    @staticmethod
    def send_admin_alert(alert_type: str, details: dict):
        """
        Send alert to admin
        """
        print(f"[ADMIN_ALERT] Type: {alert_type}")
        print(f"[ADMIN_ALERT] Details: {json.dumps(details, indent=2)}")
        return True
