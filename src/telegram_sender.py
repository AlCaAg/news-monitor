import requests
from .log import logger
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(text: str) -> bool:
    """
    Send a message to a Telegram chat.
    
    Args:
        text: The message text to send (supports HTML formatting)
        
    Returns:
        bool: True if the message was sent successfully, False otherwise
    """
    try:
        endpoint = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"⚠️ Error enviando mensaje de Telegram: {e}")
        return False
