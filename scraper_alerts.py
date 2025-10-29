#!/usr/bin/env python3
"""
News Monitor - Monitors websites for news matching specific keywords
and sends alerts via Telegram when new matches are found.
"""
import logging
from typing import List, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Import local modules
from src.config import URL, KEYWORDS, validate_config
from src.scraper_url import get_all_urls
from src.telegram_sender import send_telegram_message
from src.cache_service import load_cache, save_cache


def find_new_matches(urls: List[str], keywords: List[str], cache: Set[str]) -> List[str]:
    """
    Find URLs that match any of the keywords and haven't been seen before.
    
    Args:
        urls: List of URLs to check
        keywords: List of keywords to search for in URLs
        cache: Set of previously seen URLs
        
    Returns:
        List of new matching URLs
    """
    new_matches = []
    
    for url in urls:
        url_lower = url.lower()
        if (any(keyword in url_lower for keyword in keywords) and 
            url not in cache):
            new_matches.append(url)
            
    return new_matches


def main():
    """Main function to run the news monitoring process."""
    logging.info("🚀 Starting news monitor...")
    
    # Validate configuration
    if not validate_config():
        logging.error("❌ Configuration validation failed. Please check your environment variables.")
        return
        
    logging.info(f"🔍 Monitoring URL: {URL}")
    logging.info(f"🔑 Keywords: {', '.join(KEYWORDS)}")
    
    try:
        # Load cache and fetch URLs
        cache = load_cache()
        logging.info(f"📚 Loaded {len(cache)} URLs from cache")
        
        # Get all URLs from the target page that match our keywords
        urls = get_all_urls(URL, KEYWORDS)
        logging.info(f"🔗 Found {len(urls)} matching URLs")
        
        # Find new matches
        new_matches = find_new_matches(urls, KEYWORDS, cache)
        
        # Process new matches
        if new_matches:
            logging.info(f"🎯 Found {len(new_matches)} new matches!")
            
            # Send alerts and update cache
            for url in new_matches:
                message = f"📰 <b>New match found!</b>\n{url}"
                if send_telegram_message(message):
                    cache.add(url)
                    logging.info(f"📤 Sent alert: {url}")
                else:
                    logging.error(f"❌ Failed to send alert: {url}")
            
            # Save updated cache
            save_cache(cache)
            logging.info(f"💾 Updated cache with {len(new_matches)} new URLs")
        else:
            logging.info("😴 No new matches found.")
            
    except Exception as e:
        logging.error(f"⚠️ An error occurred: {str(e)}", exc_info=True)
    
    logging.info("🏁 Monitoring complete")


if __name__ == "__main__":
    main()
