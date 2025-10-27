# 📰 News Scraper for GitHub Actions

Scraper que revisa una página web cada 30 minutos y envía alertas por Telegram si encuentra alguna palabra clave.

## 🚀 Cómo configurarlo en GitHub Actions

1. Sube este repo a tu cuenta de GitHub.
2. Ve a **Settings → Secrets → Actions** y crea los siguientes secretos:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `URL`
   - `KEYWORDS`
3. GitHub ejecutará automáticamente el scraper cada 30 minutos.
