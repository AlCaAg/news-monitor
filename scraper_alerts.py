#!/usr/bin/env python3
"""
News Monitor - Monitors websites for news matching specific keywords
and sends alerts via Telegram when new matches are found.
"""
from typing import List, Set
from src.log import logger

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
    logger.info("🚀 Iniciando monitor de noticias...")
    
    # Validate configuration
    if not validate_config():
        logger.error("❌ Falló la validación de configuración. Por favor verifica las variables de entorno.")
        return
        
    logger.info(f"🔍 Monitoreando URL: {URL}")
    logger.info(f"🔑 Palabras clave: {', '.join(KEYWORDS)}")
    
    try:
        # Load cache and fetch URLs
        cache = load_cache()
        logger.info(f"📚 Se cargaron {len(cache)} URLs de la caché")
        
        # Get all URLs from the target page that match our keywords
        urls = get_all_urls(URL, KEYWORDS)
        logger.info(f"🔗 Se encontraron {len(urls)} URLs que coinciden")
        
        # Find new matches
        new_matches = find_new_matches(urls, KEYWORDS, cache)
        
        # Process new matches
        if new_matches:
            logger.info(f"🎯 ¡Se encontraron {len(new_matches)} nuevas coincidencias!")
            
            # Send alerts and update cache
            for url in new_matches:
                message = f"📰 <b>Noticia detectada:</b>\n{url}"
                if send_telegram_message(message):
                    cache.add(url)
                    logger.info(f"📤 Alerta enviada: {url}")
                else:
                    logger.error(f"❌ Error al enviar alerta: {url}")
            
            # Save updated cache
            save_cache(cache)
            logger.info(f"💾 Caché actualizada con {len(new_matches)} nuevas URLs")
        else:
            logger.info("😴 No se encontraron nuevas coincidencias.")
            
    except Exception as e:
        logger.error(f"❌ Ocurrió un error: {str(e)}")
        raise
    
    logger.info("🏁 Monitoreo completado")


if __name__ == "__main__":
    main()
