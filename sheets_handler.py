import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import json

def get_sheets_service():
    """Connect to Google Sheets"""
    # For now, we'll use a simple approach
    # Later you can set up a service account
    return None

def save_lead_to_sheet(sheet_id, data):
    """Save lead data to Google Sheet"""
    try:
        # This is simplified version
        # In real setup: connect with service account
        print(f"Would save to sheet: {data}")
        return True
    except Exception as e:
        print(f"Error saving to sheet: {e}")
        return False

def create_sheet_header():
    """Create header row in Google Sheet"""
    headers = ['Timestamp', 'Sender', 'Subject', 'Score', 'Level', 'Reply Sent']
    return headers