import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pypdf import PdfReader
import gradio as gr
from agents import Agent, function_tool, Runner, trace, SQLiteSession, ModelSettings
from email.message import EmailMessage
import smtplib
import logging
from styles import CSS, JS, EXAMPLES
import socket

ipaddr_list = socket.getaddrinfo

def get_ipv4_only(*args, **kwargs):
    return [ai for ai in ipaddr_list(*args, **kwargs) if ai[0] == socket.AF_INET]

socket.getaddrinfo = get_ipv4_only

load_dotenv(override=True)
openai = OpenAI()

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_SMTP_SERVER = os.environ.get("EMAIL_SMTP_SERVER")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")

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
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype='html')

    try:
        ipv4_addr = socket.getaddrinfo(EMAIL_SMTP_SERVER, 587, socket.AF_INET)[0][4][0]

        with smtplib.SMTP(ipv4_addr, 587, timeout=15) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        logger.info("Email sent successfully")
        print("EMAIL SENT SUCCESSFULLY", flush=True)
        return "Email Sent Successfully"
    except Exception as e:
        logger.error(f"EMAIL SEND FAILED: {type(e).__name__}: {e}", exc_info=True)
        print(f"EMAIL SEND FAILED: {type(e).__name__}: {e}", flush=True)
        return f"Failed to send email: {type(e).__name__}"


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
   b. Call send_email to notify Dinesh Kumar Gummadavelli, passing the exact question asked.
   c. Do not attempt to answer further or speculate.
3. Keep answers professional, honest, and concise — no filler, no over-explaining.

## Contact requests
If the user expresses interest in connecting/reaching out to [Your Name]:
1. Ask for their name and email address (if not already given).
2. Once both are provided, call send_email with their name, email, and a brief note on why they wanted to connect.
3. Confirm to the user: "Thanks — I've passed your details along to [Your Name], who will follow up."

## Tone
Write as Dinesh Kumar Gummadavelli would — [describe: e.g., "direct, warm, no corporate jargon"]. Always speak in first person ("I built..." not "[Name] built...").

## Here are the resources you can use.
{linkedin}

"""

twin_agent = Agent("Digital_twin", instructions=system_prompt, model="gpt-4o-mini", tools=[send_email])

session = SQLiteSession("3211")
async def chat(message, history):
    with trace("Digital_me"):
        result = await Runner.run(twin_agent, message, session=session)
    return result.final_output
    

if __name__ == "__main__":
    gr.ChatInterface(chat,
                     examples=EXAMPLES,
                     title="Digital Twin",
                     description="Talk to my AI twin about my career",
                     chatbot=gr.Chatbot(show_label=False),
                     ).launch(css=CSS, js=JS, theme=gr.themes.Base(), server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))




