"""Telegram notification helper with safe message handling."""

import requests
import config

def send_telegram_message(message: str) -> None:
    """
    Send a message to the configured Telegram chat.
    Splits into chunks if too long (Telegram max = 4096 chars).
    """
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"

        # Telegram allows max 4096 chars (use 4000 for safety)
        max_length = 4000  
        chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]

        for chunk in chunks:
            payload = {
                "chat_id": config.TELEGRAM_CHAT_ID,
                "text": chunk,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code != 200:
                print(f"Telegram error: {response.text}")

    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
