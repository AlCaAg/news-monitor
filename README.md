# 📰 News Monitor + Telegram Alerts

Monitoriza una página web y canales de Telegram en busca de palabras clave y envía alertas por Telegram.

## Componentes
- **scraper_alerts.py** → revisa una página cada X minutos.
- **tele_channel_monitor.py** → escucha mensajes en tiempo real en canales de Telegram.

## Despliegue en Render
1. Sube este repo a tu GitHub.
2. Entra a [Render.com](https://render.com) → "New" → "Blueprint" → conecta tu repo.
3. Render detectará `render.yaml` y creará los 2 workers.
4. Configura tus **Environment Variables**.
5. Deploy → ambos scripts se ejecutan automáticamente 24/7 🚀
