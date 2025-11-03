from typing import List
import requests
from bs4 import BeautifulSoup
from .log import logger
from urllib.parse import urljoin

def get_all_urls(site_url: str, keywords: List[str] = None) -> List[str]:
    """
    Get all URLs from the specified webpage that match any of the given keywords.
    
    Args:
        site_url: The URL of the webpage to scrape
        keywords: List of keywords to filter URLs (case-insensitive)
        
    Returns:
        List of matching URLs
    """
    try:
        response = requests.get(site_url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"❌ Error fetching {site_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    urls = set()
    
    # Extract all valid links
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href:
            continue
            
        # Convert relative URLs to absolute
        if not href.startswith(('https://')):
            href = urljoin(site_url, href)
        
        # If no keywords provided, add all URLs
        if not keywords:
            urls.add(href)
            continue
            
        # Check if any keyword is in the URL (case-insensitive)
        href_lower = href.lower()
        if any(keyword.lower() in href_lower for keyword in keywords):
            urls.add(href)

    logger.info(f"🔗 Found {len(urls)} URLs in {site_url}")
    return list(urls)
