import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_interview_confirmation(
    candidate_name,
    chat_id,
    interviewer_name,
    date,
    time,
    job_title
):

    if not TELEGRAM_BOT_TOKEN or not chat_id:
        return

    message = f"""
🎉 Interview Confirmed!

Candidate: {candidate_name}
Role: {job_title}

📅 Date: {date}
⏰ Time: {time}
👤 Interviewer: {interviewer_name}

Please join 5 minutes early.

Good luck!
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        requests.post(url, json=payload)
    except:
        pass