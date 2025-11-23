# Research Agent & UI-Agent

This repository contains two main AI-powered agents:

---

## 1. Research Agent

A conversational AI research assistant powered by Google's Gemini 2.0 Flash model and built with Pydantic AI. This agent provides clear, concise, and deeply helpful answers while maintaining conversation context.

**Features:**
- Conversational interface (CLI)
- Google Gemini 2.0 Flash integration
- Logfire monitoring and tracing
- Web research tools
- Session context memory

**Quick Start:**
```bash
cd ai-assessment/pydantic-ai/research-agent
python3 -m venv venv
source venv/bin/activate
pip install pydantic-ai google-generativeai python-dotenv logfire
python main.py
```

1. **Clone the repository and navigate to research-agent directory:**
   ```bash
   cd ai-assessment/research-agent
   ```


See the full `research-agent/README.md` for details on configuration, environment variables, troubleshooting, and contributing.

---

## 2. UI-Agent (E-Commerce Chat Assistant)

A beautiful, animated, and modern e-commerce chatbot UI built with Starlette and Python. This project features:
- Glassmorphism and gradient UI
- Animated chat bubbles and cart
- Typing indicator for the bot
- In-memory cart and chat state
- Emoji and pricing helpers
- Responsive and mobile-friendly design

**Features:**
- Add, remove, and update items in the cart via chat
- Animated, modern UI with smooth transitions
- Real-time cart updates
- Logfire integration for logging

**Quick Start:**
```bash
cd ai-assessment/pydantic-ai/ui-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 starlette_ui.py
```

The app will start on `http://localhost:8020`.

1. **Clone the repository and navigate to ui-agent directory:**
   ```bash
   cd ai-assessment/ui-agent
   ```


See the full `ui-agent/README.md` for more details, customization tips, and project structure.

