import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(trade):
    if not WEBHOOK_URL:
        print("[DISCORD ERROR] Webhook URL not set.")
        return

    message = (
        f"📢 **SPY Options Trade Alert**\n"
        f"**Direction:** {trade['direction']}\n"
        f"**Strike:** ${trade['strike']}\n"
        f"**Expiration:** {trade['expiration']}\n"
        f"**Confidence (Weighted):** {round(trade['confidence'] * 100)}%\n"
        f"**Stop Loss:** {trade['stop_loss'] * 100:.0f}%\n"
        f"**Take Profit:** {trade['take_profit'] * 100:.0f}%\n"
        f"**Strategy:** {trade['strategy']}"
    )

    payload = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"[DISCORD ERROR] Failed to send alert: {e}")
