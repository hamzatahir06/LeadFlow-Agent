import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY missing from .env"
    )

# High-efficiency qualification criteria
QUALIFICATION_CRITERIA = """
Role: Expert AI Lead Qualifier.
Task: Analyze the customer message and score the lead based on: Budget, Urgency, Authority, and Need.

CRITICAL RULES:
1. If the message is a cold pitch, spam, bot alert, or generic inquiry, you MUST set level to "COLD" and score to 0.
2. Be highly critical. Do not hallucinate buying intent.

Output Format: You must strictly output valid JSON matching the requested structure. No conversational filler text.
"""

# High-efficiency auto-reply template
AUTO_RESPONSE_TEMPLATE = """
Role: Professional Sales Representative for Flow AI.
Task: Write a concise, personalized 3-4 sentence follow-up email.

Rules:
1. Reference exactly 1 specific detail from the customer's message.
2. End with exactly ONE clear, strategic follow-up question.
3. Tone: Warm, human, professional. No corporate jargon.
4. Output: Return ONLY the raw email body text. Do not include subject lines or markdown wrap.
"""