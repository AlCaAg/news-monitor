import os
from typing import Set
from .config import CACHE_FILE
from .log import logger

def load_cache() -> Set[str]:
    """Load sent URLs from cache file."""
    if not os.path.exists(CACHE_FILE):
        return set()
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except Exception as e:
        logger.error(f"⚠️ Error loading cache: {e}")
        return set()

def save_cache(sent_urls: Set[str]) -> None:
    """Save updated URLs to cache file."""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            for url in sorted(sent_urls):
                f.write(url + "\n")
    except Exception as e:
        logger.error(f"⚠️ Error saving cache: {e}")
