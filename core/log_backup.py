import os
import shutil
from datetime import datetime

TRADE_HISTORY_JSON = "data/trade_history.json"
TRADE_HISTORY_CSV = "data/trade_history.csv"
BACKUP_DIR = "data/backups"


def backup_logs():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    os.makedirs(BACKUP_DIR, exist_ok=True)

    try:
        if os.path.exists(TRADE_HISTORY_JSON):
            shutil.copy2(TRADE_HISTORY_JSON, f"{BACKUP_DIR}/history_{timestamp}.json")
            print(f"[BACKUP] JSON backup saved: history_{timestamp}.json")
        if os.path.exists(TRADE_HISTORY_CSV):
            shutil.copy2(TRADE_HISTORY_CSV, f"{BACKUP_DIR}/history_{timestamp}.csv")
            print(f"[BACKUP] CSV backup saved: history_{timestamp}.csv")
    except Exception as e:
        print(f"[BACKUP ERROR] Failed to back up logs: {e}")
