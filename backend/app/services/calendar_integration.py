import json
from datetime import datetime, timedelta

class CalendarIntegrationService:
    """Integrate with Google Calendar and Outlook"""
    
    @staticmethod
    def sync_with_google_calendar(user_email: str, event_id: str):
        """
        Sync pass with Google Calendar event (STUB)
        In production, use Google Calendar API
        """
        print(f"[GOOGLE_CALENDAR_STUB] Syncing pass with Google Calendar")
        print(f"[GOOGLE_CALENDAR_STUB] User: {user_email}")
        print(f"[GOOGLE_CALENDAR_STUB] Event ID: {event_id}")
        
        # In production:
        # from google.auth.transport.requests import Request
        # from google.oauth2.service_account import Credentials
        # from googleapiclient.discovery import build
        
        return {
            "status": "synced",
            "calendar": "Google Calendar",
            "user": user_email,
            "event_id": event_id
        }
    
    @staticmethod
    def sync_with_outlook(user_email: str, event_id: str):
        """
        Sync pass with Outlook calendar (STUB)
        In production, use Microsoft Graph API
        """
        print(f"[OUTLOOK_STUB] Syncing pass with Outlook")
        print(f"[OUTLOOK_STUB] User: {user_email}")
        print(f"[OUTLOOK_STUB] Event ID: {event_id}")
        
        # In production:
        # Use Microsoft Graph API to sync events
        
        return {
            "status": "synced",
            "calendar": "Outlook",
            "user": user_email,
            "event_id": event_id
        }
    
    @staticmethod
    def create_pass_from_calendar_event(calendar_event: dict) -> dict:
        """
        Automatically create pass from calendar event
        """
        print(f"[CALENDAR_AUTO_PASS] Creating pass from calendar event")
        print(f"[CALENDAR_AUTO_PASS] Event: {json.dumps(calendar_event, indent=2)}")
        
        # Extract event details
        event_title = calendar_event.get('title', 'Guest')
        event_start = calendar_event.get('start_time')
        event_end = calendar_event.get('end_time')
        attendee_email = calendar_event.get('attendee_email')
        
        pass_data = {
            "guest_name": event_title,
            "guest_email": attendee_email,
            "valid_from": event_start,
            "valid_until": event_end,
            "auto_generated": True,
            "calendar_source": calendar_event.get('calendar_type', 'unknown')
        }
        
        print(f"[CALENDAR_AUTO_PASS] Pass data: {json.dumps(pass_data, indent=2)}")
        
        return pass_data
    
    @staticmethod
    def check_calendar_conflicts(guest_email: str, proposed_time: datetime, duration_hours: int):
        """
        Check for calendar conflicts
        """
        proposed_end = proposed_time + timedelta(hours=duration_hours)
        
        print(f"[CALENDAR_CHECK] Checking conflicts for {guest_email}")
        print(f"[CALENDAR_CHECK] Time: {proposed_time} to {proposed_end}")
        
        # In production: Check Google Calendar and Outlook for conflicts
        
        return {
            "conflicts": [],
            "is_available": True
        }
