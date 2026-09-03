---
title: Digital_me
app_file: app.py
sdk: gradio
sdk_version: 6.20.0
---

# Digital Twin

An AI agent that answers questions about my (Dinesh Kumar Gummadavelli's) career, in first person, as if it were me — built on the OpenAI Agents SDK and served through a Gradio chat UI.

## What it does

- Answers career-related questions (work experience, skills, projects, education) using my LinkedIn profile as its knowledge base.
- Stays in scope — if asked something outside my professional background, it says so instead of guessing.
- If it doesn't know the answer, it pings me directly on Telegram with the question. My reply is routed back into the same chat session automatically, so the visitor never has to leave the page.
- If a visitor wants to be put in touch with me directly (an opportunity, a collaboration, etc.), it collects their name and email and sends me an email.

## How it works

- `app.py` — the whole app: the agent, its two tools (`send_email`, `contact_dinesh`), the Gradio UI, and a small FastAPI route that receives Telegram webhook replies and routes them back to the right chat session via a polling `gr.Timer`.
- `styles.py` — custom CSS/JS for the chat UI theme.
- `main.ipynb` — local prototyping notebook; superseded by `app.py`.
- `linkedin.pdf` — my LinkedIn export, parsed at startup and given to the agent as context.

## Tech stack

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (`gpt-4o-mini`)
- [Gradio](https://www.gradio.dev/) for the chat interface
- FastAPI + Uvicorn, mounted alongside Gradio, for the Telegram webhook
- `pypdf` for reading the LinkedIn export

## Running locally

```bash
git clone https://github.com/Dinesh3250/Digital-me.git
cd Digital-me
uv sync            # or: pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
OPENAI_API_KEY=
EMAIL_ADDRESS=
EMAIL_SMTP_SERVER=
EMAIL_APP_PASSWORD=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Then run:

```bash
uv run app.py       # or: python app.py
```

The app starts on `http://localhost:7860` (or `$PORT` if set).

## Deployment

Configured to run on platforms like Render or Hugging Face Spaces — set the same environment variables above as secrets on the platform, and point the Telegram bot's webhook at `https://<your-deployed-url>/telegram_webhook`.
