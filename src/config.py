import os
from .log import logger

# Load environment variables
URL = os.getenv("URL")
KEYWORDS = [k.strip().lower() for k in os.getenv("KEYWORDS").split(",") if k.strip()]
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CACHE_FILE = "sent_alerts.txt"

def validate_config() -> bool:
    """Validate that all required environment variables are set."""
    required_vars = ["URL", "KEYWORDS", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
    missing = [var for var in required_vars if not globals().get(var)]
    
    if missing:
        logger.error(f"❌ Faltan variables de entorno requeridas: {', '.join(missing)}")
        return False
    return True
