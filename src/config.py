import os
from typing import List

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
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        return False
    return True
