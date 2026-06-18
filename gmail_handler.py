import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
def authenticate_gmail():
    """Login to Gmail once, save permission"""
    creds = None
    
    # Check if we already have saved login
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no saved login, ask user to login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save for next time
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_gmail_service():
    """Connect to Gmail"""
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_unread_emails(service):
    """Get unread emails from inbox"""
    try:
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=5  # Get last 5 unread
        ).execute()
        
        messages = results.get('messages', [])
        return messages
    except Exception as e:
        print(f"Error reading emails: {e}")
        return []

def get_email_details(service, message_id):
    """Read one email and get sender, subject, body"""
    try:
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        
        headers = message['payload']['headers']
        sender = next(h['value'] for h in headers if h['name'] == 'From')
        subject = next(h['value'] for h in headers if h['name'] == 'Subject')
        
        # Get body
        if 'parts' in message['payload']:
            body = message['payload']['parts'][0]['body'].get('data', '')
        else:
            body = message['payload']['body'].get('data', '')
        
        if body:
            body = base64.urlsafe_b64decode(body).decode('utf-8')
        
        return {
            'id': message_id,
            'sender': sender,
            'subject': subject,
            'body': body
        }
    except Exception as e:
        print(f"Error getting email details: {e}")
        return None

def send_email(service, to, subject, body):
    """Send reply email"""
    try:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}
        
        service.users().messages().send(
            userId='me',
            body=send_message
        ).execute()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def mark_as_read(service, message_id):
    """Mark email as read after processing"""
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        return True
    except Exception as e:
        print(f"Error marking as read: {e}")
        return False