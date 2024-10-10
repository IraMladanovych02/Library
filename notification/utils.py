import os
import requests
from dotenv import load_dotenv


load_dotenv()


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage"
    payload = {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "text": message
    }
    requests.post(url, json=payload)
