import os
import requests
from bs4 import BeautifulSoup

URL = os.getenv("URL", "https://www.ejemplo.com/noticias")
KEYWORDS = os.getenv("KEYWORDS", "colombia,economía,bitcoin").split(",")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)

def check_news():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()
        for kw in KEYWORDS:
            if kw.lower() in text:
                send_telegram_alert(f"🔍 Palabra clave encontrada: {kw}\nURL: {URL}")
                break
    except Exception as e:
        send_telegram_alert(f"⚠️ Error en el scraper: {e}")

if __name__ == "__main__":
    check_news()
