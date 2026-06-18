import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_slack_notification(level, score, sender):
    """Send notification to Slack"""
    webhook = os.getenv('SLACK_WEBHOOK')
    
    if not webhook:
        print("⚠️ No Slack webhook configured")
        return False
    
    # Choose emoji based on level
    emoji = "🔥" if level == "HOT" else "🟡" if level == "WARM" else "❄️"
    
    message = {
        "text": f"{emoji} New Lead Processed!",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{emoji} New {level} Lead*\n\nFrom: {sender}\nScore: {score}/100"
                }
            }
        ]
    }
    
    try:
        response = requests.post(webhook, json=message)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending Slack notification: {e}")
        return False