import os
import requests
from bs4 import BeautifulSoup
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuración general
URL = os.getenv("URL")
KEYWORDS = os.getenv("KEYWORDS").split(",")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CACHE_FILE = "sent_alerts.txt"


def send_telegram_alert(message):
    """Envía un mensaje al chat de Telegram."""
    try:
        api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        response = requests.post(api_url, data=data, timeout=10)
        logging.info(f"📤 Enviando mensaje a Telegram...")
        logging.info(f"Status code: {response.status_code}")
        logging.info(f"Response: {response.text}")
        if response.status_code == 200:
            logging.info("✅ Mensaje enviado correctamente.")
        else:
            logging.warning("⚠️ No se pudo enviar el mensaje.")
    except Exception as e:
        logging.error(f"Error enviando alerta a Telegram: {e}")


def load_sent_alerts():
    """Carga las URLs ya notificadas."""
    if not os.path.exists(CACHE_FILE):
        return set()
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())


def save_sent_alert(url):
    """Guarda la URL de una noticia ya notificada."""
    with open(CACHE_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")


def check_news():
    """Scrapea la página y busca coincidencias de palabras clave en URLs."""
    logging.info(f"🔍 Analizando sitio: {URL}")
    logging.info(f"Palabras claves configuradas: {KEYWORDS}")

    sent_alerts = load_sent_alerts()

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.select("div.td_module_flex a[href]")
        found = False

        for a_tag in articles:
            href = a_tag["href"]
            title = a_tag.get("title", href)
            lower_href = href.lower()

            # Buscar palabra clave en URL
            for kw in KEYWORDS:
                if kw.lower() in lower_href:
                    if href in sent_alerts:
                        logging.info(f"⏭️ Ya se notificó esta URL: {href}")
                    else:
                        found = True
                        message = (
                            f"📰 <b>Nueva noticia detectada</b>\n\n"
                            f"🔎 <b>Palabra clave:</b> <code>{kw}</code>\n"
                            f"🧾 <b>Título:</b> {title}\n"
                            f"🌐 <b>Enlace:</b> {href}\n\n"
                            f"🕒 <i>Detectado automáticamente por tu bot</i>"
                        )
                        send_telegram_alert(message)
                        save_sent_alert(href)
                        logging.info(f"✅ Noticia enviada: {href}")

        if not found:
            logging.info("😴 No se encontraron coincidencias nuevas.")

    except Exception as e:
        logging.error(f"Error al analizar la página: {e}")
        send_telegram_alert(f"⚠️ <b>Error en el scraper:</b> {e}")


if __name__ == "__main__":
    logging.info("🚀 Iniciando ejecución del scraper...")
    check_news()
    logging.info("✅ Ejecución completada.")
