import schedule
import time
from google import genai
from config import GEMINI_API_KEY, QUALIFICATION_CRITERIA, AUTO_RESPONSE_TEMPLATE
from gmail_handler import (
    get_gmail_service, get_unread_emails, 
    get_email_details, send_email, mark_as_read
)
from slack_handler import send_slack_notification
import json
from datetime import datetime
import os

# Setup Gemini
client = genai.Client(
    api_key=GEMINI_API_KEY
)

def analyze_lead(customer_message):
    """Analyze email and score it"""
    prompt = f"""
    {QUALIFICATION_CRITERIA}
    
    CUSTOMER MESSAGE:
    {customer_message}
    
    Respond ONLY as JSON (no other text):
    {{
        "score": <number 0-100>,
        "level": "<HOT/WARM/COLD>",
        "why": "<1-2 sentences>",
        "key_points": ["point1", "point2"]
    }}
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
    )
        return response.text

    except Exception as e:
        print(f"❌ Gemini Analysis Error: {e}")
        
        return json.dumps({
            "score": 0,
            "level": "COLD",
            "why": "Gemini analysis failed",
            "key_points": []
        })
    
def generate_auto_reply(customer_message,qualification_level):
    """Generate smart reply"""
    prompt = f"""
    {AUTO_RESPONSE_TEMPLATE}
    
    CUSTOMER MESSAGE:
    {customer_message}
    
    LEAD LEVEL: {qualification_level}
    
    Write a friendly email reply (just the email body, 3-10 lines):
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
    )
        return response.text

    except Exception as e:
        print(f"❌ Gemini Reply Error: {e}")

        return (
            "Thank you for reaching out. "
            "We received your message and will review it shortly."
        )

def process_email(service, email):
    """Process ONE email"""
    print(f"\n📧 Processing email: {email['id']}")
    
    details = get_email_details(service, email['id'])
    if not details:
        return False
    
    sender = details['sender']
    subject = details['subject']
    body = details['body']
    
    print(f"From: {sender}")
    print(f"Subject: {subject}")
    
    # 1. Immediate Bot/Alert Filtering
    banned_keywords = ["no-reply", "security alert", "mailer-daemon", "google workspace", "subscription"]
    combined_text = (sender + " " + subject).lower()

    if any(keyword in combined_text for keyword in banned_keywords):
        print("⚠️ Skipping: Automated system email or alert detected.")
        mark_as_read(service, email['id'])
        return False

    # 2. AI Lead Analysis
    print("🤔 Analyzing...")
    analysis_text = analyze_lead(body)
    
    clean_text = analysis_text.strip()
    if clean_text.startswith("```"):
        clean_text = (
            clean_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )
    
    try:
        analysis = json.loads(clean_text)
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        analysis = {
            "score": 0,
            "level": "COLD",
            "why": "JSON parsing failed",
            "key_points": []
            }
    
    score = analysis.get('score', 0)
    level = analysis.get('level', 'UNKNOWN')
    
    print(f"✅ Score: {score}/100 | Level: {level}")
    
    # 3. Handle Cold Leads / Spam
    if level == "COLD" or score < 40:
        print("🤫 Cold lead or spam detected. Skipping auto-reply.")
        mark_as_read(service, email['id'])
        save_result(sender, subject, score, level, "NO_REPLY_SPAM_OR_COLD")
        return True

    # 4. Generate & Send Auto-Reply for HOT/WARM leads
    print("✍️ Generating reply...")
    reply = generate_auto_reply(body, level)

    print("📨 Sending reply...")
    reply_subject = f"Re: {subject}"
    sent = send_email(service, sender, reply_subject, reply)
    
    if sent:
        print("✅ Reply sent!")
        mark_as_read(service, email['id'])
        send_slack_notification(level, score, sender)
        save_result(sender, subject, score, level, reply)
        return True
    else:
        print("❌ Failed to send reply")
        return False


def save_result(sender, subject, score, level, reply):
    """Save result to file"""

    os.makedirs("results", exist_ok=True)

    result = {
        "timestamp": datetime.now().isoformat(),
        "sender": sender,
        "subject": subject,
        "score": score,
        "level": level,
        "reply": reply
    }

    filename = (
        f"results/agent_lead_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"💾 Saved to {filename}")    
   

def run_agent():
    """Main agent loop"""
    print(f"\n{'='*100}")
    print(f"🤖 Agent Running at {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*100}")
    
    try:
        service = get_gmail_service()
        unread = get_unread_emails(service)
        
        if not unread:
            print("✨ No new emails. Sleeping...")
        else:
            print(f"📬 Found {len(unread)} unread emails")
            for email in unread:
                process_email(service, email)
    
    except Exception as e:
        print(f"❌ Agent error: {e}")

def schedule_agent():
    """Schedule agent to run every 10 minutes"""
    schedule.every(10).minutes.do(run_agent)
    print("🚀 Agent scheduled! Running every 10 minutes...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_agent()       # Run once 10 immediately on startup
    schedule_agent()  # Start the 10-minute repetition loop    