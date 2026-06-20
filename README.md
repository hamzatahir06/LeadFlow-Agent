# 🤖 EmailAutomaton - Autonomous Lead Qualifier Agent

An intelligent, autonomous AI agent that automatically reads Gmail, qualifies leads, and sends personalized replies 24/7 without human intervention.

## ✨ Key Features

✅ **Fully Autonomous** - Runs 24/7 automatically, no manual intervention  
✅ **AI-Powered Lead Scoring** - Classifies leads as HOT/WARM/COLD with intelligent analysis  
✅ **Smart Email Replies** - Generates contextual, professional responses automatically  
✅ **Real-Time Slack Notifications** - Get instant alerts for new qualified leads  
✅ **100% Free** - Uses free APIs (Gemini, Gmail, Slack)  
✅ **No Database Required** - Saves data locally as JSON  
✅ **Production Ready** - Deployable to cloud for 24/7 operation  

## 🎯 What It Does

```
Gmail Inbox → Agent Checks Every 5 Mins
           ↓
         AI Analyzes Email (Budget, Urgency, Decision-Maker)
           ↓
         Scores Lead 0-100 (HOT/WARM/COLD)
           ↓
         Generates Smart Reply
           ↓
         Sends Reply Automatically
           ↓
         Saves Record + Slack Notification
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Gmail account
- Slack workspace (optional)
- Gemini API key (free)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/hamzatahir06/EmailAutomaton.git
cd EmailAutomaton
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Google API Credentials**
   - Go to https://console.cloud.google.com/
   - Create new project
   - Enable Gmail API
   - Create OAuth 2.0 Desktop credentials
   - Download as `gmail_credentials.json`

4. **Get Gemini API Key**
   - Go to https://aistudio.google.com/app/apikey
   - Create free API key

5. **Get Slack Webhook (Optional)**
   - Go to https://api.slack.com/apps
   - Create app → Incoming Webhooks
   - Copy webhook URL

6. **Create `.env` file**
```
GEMINI_API_KEY=your_key_here
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR_WEBHOOK
```

7. **Run**
```bash
python agent.py
```

## 📊 How It Works

### Lead Qualification
- **HOT (85-100)** - High priority, budget + urgency + decision-maker
- **WARM (60-84)** - Good potential, needs nurturing
- **COLD (0-59)** - Low priority, general interest

### Process
1. Reads Gmail inbox every 5 mins
2. Analyzes email content with AI
3. Scores and classifies lead
4. Generates smart reply
5. Sends automatically from your Gmail
6. Saves record locally
7. Sends Slack notification

## 🛠️ Tech Stack

- **AI:** Gemini 1.5 Flash (free)
- **Email:** Gmail API
- **Notifications:** Slack Webhooks
- **Language:** Python 3.8+
- **Storage:** JSON files

## 📁 Project Structure

```
EmailAutomaton/
├── agent.py              # Main agent logic
├── config.py            # Configuration
├── gmail_handler.py     # Gmail API
├── slack_handler.py     # Slack integration
├── requirements.txt     # Dependencies
├── gmail_credentials.json
├── .env                 # API keys (in .gitignore)
├── .gitignore
├── README.md
└── results/            # Saved records
```

## ⚙️ Configuration

Edit `config.py` to customize lead scoring and email replies:

```python
QUALIFICATION_CRITERIA = """
You are a lead qualification expert. Analyze if this customer is HIGH PRIORITY.
Check for: Budget, Urgency, Decision-maker, Real need
"""

AUTO_RESPONSE_TEMPLATE = """
Write a SHORT, intelligent follow-up email.
Rules: Reference details, ask ONE question, 3-4 sentences, sound human
"""
```

## 🔄 Usage

### Run Once
```bash
python agent.py
```

### Run 24/7 (Every 5 mins)
Edit `agent.py` last line:
```python
if __name__ == "__main__":
    run_agent()
    schedule_agent()
```

### View Results
Check `results/` folder for JSON files with all processed leads

## 🚀 Deploy to Cloud (24/7)

### Render (Free)
1. Push to GitHub
2. Go to https://render.com/
3. New → Web Service
4. Connect repo
5. Add `.env` variables
6. Deploy

Agent now runs 24/7 ☁️

## 🔐 Security

Never commit to GitHub:
```
token.pickle
.env
```

Add to `.gitignore`:
```
token.pickle
.env
*.pyc
__pycache__/
results/
```

## ❓ Troubleshooting

**Gmail 403 Error:**
- Configure OAuth consent screen
- Add email as test user

**Model Not Found:**
- Verify Gemini API key
- Try `gemini-pro` instead

**No Slack Notifications:**
- Check webhook URL
- Verify it's in `.env`

## 📈 Future Features

- [ ] Cloud deployment (24/7)
- [ ] Google Sheets tracking
- [ ] Analytics dashboard
- [ ] Email sequences
- [ ] CRM integration
- [ ] Custom rules

## 📝 License

MIT - Free to use and modify

---

**🤖 Autonomous AI Agent for Lead Qualification | Production Ready**
