import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pypdf import PdfReader
import gradio as gr
from agents import Agent, function_tool, Runner, trace, SQLiteSession, RunContextWrapper
from email.message import EmailMessage
import smtplib
from collections import defaultdict
from fastapi import FastAPI, Request as FastAPIRequest
import uvicorn
from dataclasses import dataclass
import socket
import logging
from styles import CSS, JS, EXAMPLES
from collections import defaultdict

MESSAGE_LIMIT = 5
session_message_count = defaultdict(int)

load_dotenv(override=True)
openai = OpenAI()

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
RESEND_HTTPS_SERVER = os.environ.get("RESEND_HTTPS_SERVER")
TELEGRAM_BOT_TOKEN= os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

logger = logging.getLogger(__name__)

@function_tool
def send_email(subject: str, text_body: str, html_body: str) -> str:
    """
    Sends an email with the given subject, text body, and HTML body to the specified recipient.

    Args:
        subject (str): The subject of the email.
        text_body (str): The plain text content of the email.
        html_body (str): The HTML content of the email.

    """
    try:
        resp = requests.post(
            RESEND_HTTPS_SERVER,
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from": "Digital Twin <onboarding@resnd.dev",
                "to": EMAIL_ADDRESS,
                "subject": subject,
                "text": text_body,
                "html": html_body,
            },
            timeout=15,
        )
        resp.raise_for_status()
        logger.info("Email sent successfully")
        print("EMAIL SENT SUCCESSFULLY", flush=True)
        return "Email Sent Successfully"
    except Exception as e:
        logger.error(f"EMAIL SEND FAILED: {type(e).__name__}: {e}", exc_info=True)
        print(f"EMAIL SEND FAILED: {type(e).__name__}: {e}", flush=True)
        return f"Failed to send email: {type(e).__name__}"
    


message_to_session = {}              # telegram message_id -> session_id
session_replies = defaultdict(list)  # session_id -> list of unread replies

def send_to_telegram(text: str) -> int:
    resp = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["result"]["message_id"]


@dataclass
class TwinContext:
    session_id: str


@function_tool
def contact_dinesh(ctx: RunContextWrapper[TwinContext], question: str) -> str:
    """
    Sends a message to Dinesh via Telegram when the AI doesn't know
    an asnwer or the user wants to be connected with him personally.

    Arguments:
    question(string) : The question or message to send to Dinesh.
    """

    session_id = ctx.context.session_id
    tagged_text = f"Message from your site (session {session_id}):\n\n {question}"
    msg_id = send_to_telegram(tagged_text)
    message_to_session[msg_id] = {"session_id": session_id, "question": question}
    return "I've sent your message to Dinesh. He will get back to you soon!"





reader = PdfReader("linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    linkedin += text
print(linkedin)

system_prompt = f"""
You are Dinesh Kumar Gummadavelli's Digital Twin — an AI agent that answers questions on Dinesh Kumar Gummadavelli's behalf, in first person, as if you were them.

## Scope
Only answer questions related to Dinesh Kumar Gummadavelli's career: work experience, skills, projects, education, and professional background.
If a question falls outside this scope, respond: "I can only answer questions about my professional background — happy to help with that instead."

## Answering rules
1. Only answer using the information provided in your knowledge/resources. Never guess, infer beyond what's given, or fabricate details.
2. If you don't know the answer (it's career-related but not covered by your resources):
   a. Tell the user honestly that you don't have that information.
   b. Call contact_dinesh, passing the exact question asked.
   c. Let the user know that Dinesh will personally respond, and that his reply will appear right here in this chat once he does — they don't need to do anything else or leave the page.
   d. Do not attempt to answer further or speculate.
3. Keep answers professional, honest, and concise — no filler, no over-explaining.

## Contact requests
If the user expresses interest in connecting/reaching out to Dinesh directly (e.g. wants to discuss an opportunity, collaborate, or just talk):
1. Ask for their name and email address (if not already given).
2. Once both are provided, call send_email with their name, email, and a brief note on why they wanted to connect.
3. Confirm to the user: "Thanks — I've passed your details along to Dinesh, who will follow up."

## Tool selection
- Use contact_dinesh when you don't know the answer to a career-related question and need Dinesh to personally weigh in — this notifies him via Telegram, and his reply will be automatically shown in this same conversation.
- Use send_email only for contact requests where the user wants Dinesh to follow up with them separately outside of this chat (e.g. via their own email), not for questions needing an in-chat answer.
- Never call both tools for the same request — pick whichever one matches what the user actually needs.

## Tone
Write as Dinesh Kumar Gummadavelli would — [describe: e.g., "direct, warm, no corporate jargon"]. Always speak in first person ("I built..." not "Dinesh built...").

## Here are the resources you can use.
{linkedin}

"""

twin_agent = Agent("Digital_twin", instructions=system_prompt, model="gpt-4o-mini", tools=[send_email, contact_dinesh])
session = SQLiteSession("32")
async def chat(message, history, request: gr.Request):
    session_id = request.session_hash

    if session_message_count[session_id] >= MESSAGE_LIMIT:
        return (
            "You've reached the message limit for this session — thanks for chatting! "
            "Feel free to start a new session, or reach out to Dinesh directly if you'd "
            "like to continue the conversation."
        )

    session_message_count[session_id] += 1

    with trace("Digital_me"):
        result = await Runner.run(twin_agent, message, context=TwinContext(session_id=session_id), session=session)
    return result.final_output



def poll_for_reply(history, request: gr.Request):
    session_id = request.session_hash
    replies = session_replies.pop(session_id, [])
    if not replies:
        return gr.skip()
    for r in replies:
        history.append({
            "role": "assistant",
            "content": r["answer"],
            "metadata": {"title": f'💬 Dinesh replied to: "{r["question"]}"'}
            })
    return history

with gr.Blocks(css=CSS, js=JS, theme=gr.themes.Base()) as demo:
    chat_interface = gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False)
    )
    timer = gr.Timer(15)
    timer.tick(
        poll_for_reply,
        inputs=[chat_interface.chatbot],
        outputs=[chat_interface.chatbot],
    )


app = FastAPI()

@app.post("/telegram_webhook")
async def telegram_webhook(request: FastAPIRequest):
    update = await request.json()
    message = update.get("message", {})
    reply_to = message.get("reply_to_message")

    if reply_to:
        original_msg_id = reply_to.get("message_id")
        record = message_to_session.get(original_msg_id)
        if record:
            session_replies[record["session_id"]].append({
                "question": record["question"],
                "answer": message.get("text", "")
            })
    return {"ok": True}


app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)



