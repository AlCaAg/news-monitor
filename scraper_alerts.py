import os
import requests
from bs4 import BeautifulSoup
import logging

# =======================
# 🔧 CONFIGURACIÓN
# =======================
URL = os.getenv("URL")
KEYWORDS = [k.strip().lower() for k in os.getenv("KEYWORDS", "").split(",")]
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CACHE_FILE = "sent_alerts.txt"

# =======================
# 🧰 LOGGING CONFIG
# =======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =======================
# 🧠 FUNCIONES AUXILIARES
# =======================
def load_cache():
    """Carga URLs ya enviadas desde el archivo de caché"""
    if not os.path.exists(CACHE_FILE):
        return set()
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_cache(sent_urls):
    """Guarda las URLs actualizadas en el archivo de caché"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        for url in sorted(sent_urls):
            f.write(url + "\n")

def send_telegram_message(text):
    """Envía mensaje al canal de Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("❌ TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no configurados")
        return

    endpoint = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    response = requests.post(endpoint, data=payload)
    if response.status_code != 200:
        logging.error(f"⚠️ Error enviando mensaje: {response.status_code} - {response.text}")

def get_all_urls(site_url):
    """Obtiene todas las URLs de la página especificada."""
    try:
        response = requests.get(site_url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"❌ Error al obtener {site_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    urls = set()

    # Extrae todos los enlaces válidos
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            urls.add(href)
        elif href.startswith("/"):
            base = site_url.rstrip("/")
            urls.add(base + href)

    logging.info(f"🔗 Se encontraron {len(urls)} URLs en {site_url}")
    return list(urls)

# =======================
# 🚀 FUNCIÓN PRINCIPAL
# =======================
def main():
    logging.info("🚀 Iniciando ejecución del scraper...")
    if not URL or not KEYWORDS:
        logging.error("❌ Variables de entorno URL o KEYWORDS no configuradas.")
        return

    logging.info(f"🔍 Analizando sitio: {URL}")
    logging.info(f"🧩 Palabras clave: {KEYWORDS}")

    cache = load_cache()
    urls = get_all_urls(URL)
    new_alerts = []

    for link in urls:
        link_lower = link.lower()
        # Revisa TODAS las palabras clave
        if any(keyword in link_lower for keyword in KEYWORDS):
            if link not in cache:
                new_alerts.append(link)
                cache.add(link)

    if new_alerts:
        for url in new_alerts:
            message = f"📰 <b>Noticia detectada:</b>\n{url}"
            send_telegram_message(message)
            logging.info(f"📢 Enviada alerta: {url}")
        save_cache(cache)
        logging.info(f"✅ {len(new_alerts)} nuevas alertas enviadas.")
    else:
        logging.info("😴 No se encontraron coincidencias nuevas.")

    logging.info("🏁 Ejecución completada.")

# =======================
# 🏃‍♂️ EJECUCIÓN
# =======================
if __name__ == "__main__":
    main()
