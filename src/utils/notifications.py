import requests
from config import TELEGRAM_BOT_TOKEN

def send_telegram_message(bot_token, chat_id, message):
    """
    Send a message via Telegram bot.
    :param bot_token: Telegram bot token.
    :param chat_id: Chat ID to send the message to.
    :param message: The message to send.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print("Notification sent successfully.")
