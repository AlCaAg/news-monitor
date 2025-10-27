import os
import asyncio
from telethon import TelegramClient, events
import requests

TG_API_ID = int(os.getenv("TG_API_ID", "0"))
TG_API_HASH = os.getenv("TG_API_HASH", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHANNELS = [ch.strip() for ch in os.getenv("CHANNELS", "@canal1").split(",")]
KEYWORDS = os.getenv("KEYWORDS", "colombia,economía,bitcoin").split(",")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)

async def main():
    client = TelegramClient("session_monitor", TG_API_ID, TG_API_HASH)

    @client.on(events.NewMessage(chats=CHANNELS))
    async def handler(event):
        text = event.raw_text.lower()
        for kw in KEYWORDS:
            if kw.lower() in text:
                msg = f"📢 Coincidencia en canal {event.chat.title}:\n{event.message.message}"
                send_telegram_alert(msg)
                break

    await client.start()
    print("🟢 Monitor de canales iniciado.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
