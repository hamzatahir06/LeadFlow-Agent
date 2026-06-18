import schedule
import time
import google.generativeai as genai
from config import GEMINI_API_KEY, QUALIFICATION_CRITERIA, AUTO_RESPONSE_TEMPLATE
from gmail_handler import (
    get_gmail_service, get_unread_emails, 
    get_email_details, send_email, mark_as_read
)
from slack_handler import send_slack_notification
import json
from datetime import datetime

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.1-flash-lite')

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
    
    response = model.generate_content(prompt)
    return response.text

def generate_auto_reply(customer_message, qualification_level):
    """Generate smart reply"""
    prompt = f"""
    {AUTO_RESPONSE_TEMPLATE}
    
    CUSTOMER MESSAGE:
    {customer_message}
    
    LEAD LEVEL: {qualification_level}
    
    Write a friendly email reply (just the email body, 3-5 lines):
    """
    
    response = model.generate_content(prompt)
    return response.text

def process_email(service, email):
    """Process ONE email"""
    print(f"\n📧 Processing email: {email['id']}")
    
    # Get full email details
    details = get_email_details(service, email['id'])
    if not details:
        return
    
    sender = details['sender']
    subject = details['subject']
    body = details['body']
    
    print(f"From: {sender}")
    print(f"Subject: {subject}")
    
    # Step 1: Analyze
    print("🤔 Analyzing...")
    analysis_text = analyze_lead(body)
    
    # Clean JSON
    clean_text = analysis_text.strip()
    if clean_text.startswith('```json'):
        clean_text = clean_text.replace('```json', '').replace('```', '')
    
    try:
        analysis = json.loads(clean_text)
    except:
        analysis = {"score": 50, "level": "WARM", "why": "Couldn't parse", "key_points": []}
    
    score = analysis.get('score', 0)
    level = analysis.get('level', 'UNKNOWN')
    
    print(f"✅ Score: {score}/100 | Level: {level}")
    
    # Step 2: Generate reply
    print("✍️ Generating reply...")
    reply = generate_auto_reply(body, level)
    
    # Step 3: Send reply
    print("📨 Sending reply...")
    reply_subject = f"Re: {subject}"
    sent = send_email(service, sender, reply_subject, reply)
    
    if sent:
        print("✅ Reply sent!")
        
        # Step 4: Mark as read
        mark_as_read(service, email['id'])
        
        # Step 5: Send Slack notification
        send_slack_notification(level, score, sender)
        
        # Save record
        save_result(sender, subject, score, level, reply)
        return True
    else:
        print("❌ Failed to send reply")
        return False

def save_result(sender, subject, score, level, reply):
    """Save result to file"""
    result = {
        "timestamp": datetime.now().isoformat(),
        "sender": sender,
        "subject": subject,
        "score": score,
        "level": level,
        "reply": reply
    }
    
    filename = f"results/agent_lead_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"💾 Saved to {filename}")

def run_agent():
    """Main agent loop - runs every 5 minutes"""
    print(f"\n{'='*50}")
    print(f"🤖 Agent Running at {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")
    
    try:
        # Connect to Gmail
        service = get_gmail_service()
        
        # Get unread emails
        unread = get_unread_emails(service)
        
        if not unread:
            print("✨ No new emails. Sleeping...")
        else:
            print(f"📬 Found {len(unread)} unread emails")
            
            # Process each email
            for email in unread:
                process_email(service, email)
    
    except Exception as e:
        print(f"❌ Agent error: {e}")

def schedule_agent():
    """Schedule agent to run every 5 minutes"""
    schedule.every(5).minutes.do(run_agent)
    
    print("🚀 Agent scheduled! Running every 5 minutes...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_agent()

    # runs after every 5 minutes schedule:
    schedule_agent()