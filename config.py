import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Example: What kind of customers do you want?
QUALIFICATION_CRITERIA = """
You are a lead qualification expert. Analyze if this customer is a HIGH PRIORITY lead.

Check for:
1. Budget mentioned? (good sign)
2. Urgency? (need it fast? good sign)
3. Decision maker? (they can say YES? good sign)
4. Real need? (or just browsing?)

Score: HOT (100-85), WARM (84-60), COLD (59-0)
"""

AUTO_RESPONSE_TEMPLATE = """
You are a professional sales representative. Write a SHORT, intelligent follow-up email.

Rules:
- Reference specific details from customer message
- Ask ONE smart follow-up question
- Sound professional, warm, human
- 3-4 sentences MAX
- Include your name and contact

Example: Thank you for reaching out about [SPECIFIC NEED]. 
We specialize in building Automation Agents for Companies. Quick question: [SMART QUESTION]?
Best, Flow AI
"""
