import os
import requests
from bs4 import BeautifulSoup

URL = os.getenv("URL")
KEYWORDS = os.getenv("KEYWORDS").split(",")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    print("Enviando alerta...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data, timeout=10)

def check_news():
    print("Iniciando scraper...")
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()
        for kw in KEYWORDS:
            if kw.lower() in text:
                print(f"Palabra clave encontrada: {kw}")
                message = (
                    f"📰 <b>Noticia detectada</b>\n\n"
                    f"🔎 <b>Palabra clave:</b> <code>{kw}</code>\n"
                    f"🌐 <b>Fuente:</b> {URL}\n\n"
                    f"🕒 <i>Detectado automáticamente por tu bot de monitoreo</i>"
                )
                send_telegram_alert(message)
            else:
                print(f"Palabra clave no encontrada: {kw}")
    except Exception as e:
        send_telegram_alert(f"Error en el scraper: {e}")
        print("Error en el scraper: ", e)

if __name__ == "__main__":
    check_news()
