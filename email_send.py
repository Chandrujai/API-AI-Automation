import os
import requests
import smtplib
from email.message import EmailMessage
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
client = OpenAI()

sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("EMAIL_APP_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")

print("Step 1: Fetching live weather data...")
url = "https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true"
weather_data = requests.get(url).json()['current_weather']

print("Step 2: Sending data to OpenAI to draft your email...")
prompt = f"""
Here is the live weather data for London:
{weather_data}

Write a short, friendly, and engaging morning or evening weather update email body. Keep it concise.
"""

ai_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)
email_body = ai_response.choices[0].message.content

print("Step 3: Sending the AI-generated email...")
msg = EmailMessage()
msg["Subject"] = "Your Automated Daily AI Weather Report"
msg["From"] = sender_email
msg["To"] = receiver_email
msg.set_content(email_body)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(sender_email, app_password)
    smtp.send_message(msg)

print("Pipeline Complete! Check your email inbox.")