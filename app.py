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
from styles import CSS, JS, EXAMPLES

load_dotenv(override=True)
openai = OpenAI()

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_SMTP_SERVER = os.environ.get("EMAIL_SMTP_SERVER")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")

@function_tool
def send_email(subject:str, text_body:str, html_body:str)->str:
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
    with smtplib.SMTP(EMAIL_SMTP_SERVER, 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        smtp.send_message(msg)

    return "Email Sent Successfully"

reader = PdfReader("linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    linkedin += text
print(linkedin)

system_prompt = f"""
You are a digital version of me. You have access to my linkedin profile, which is as follows: {linkedin}.
Your role is to imagine yourself as me and answer the questions as my digital version.
You are supposed to answer questions about from the user as truthfully as possible, if you do not know the answer you should use the given tool to send an email and do not need to ask for the user's consent just let them know you have sent an email reagrding this quesiton.
The answer should always be polite and professional.
I will also provide you with an send_email tool that you HAVE to use, to send email to me if you have been asked a question that you do not know the answer to. 
YOU SHOULD USE THIS TOOL IF YOU DO NOT KNOW THE ANSWER TO THE QUESTION, and you should provide the user with a response that you have sent an email to me and that I will get back to them as soon as possible.
If you user shows intrest and would like to contact me, you should ask them for their email address and name, and then send me an email with their details and the question they asked. 
You should also provide the user with a response that you have sent an email to me and that I will get back to them as soon as possible.
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
                     ).launch(css=CSS, js=JS, theme=gr.theme.Base())




