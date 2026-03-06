import requests

BOT_TOKEN = "8665305199:AAHkbDMiZk6EE5uTyR6YKX25JGI0StgwioE"
CHAT_ID = "1700533563"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": "🔥 Fire Guardian Test Alert"}
)