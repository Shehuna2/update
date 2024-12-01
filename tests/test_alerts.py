import requests
from src.utils.notifications import send_telegram_message
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_test_message():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": "Test message"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    send_test_message()