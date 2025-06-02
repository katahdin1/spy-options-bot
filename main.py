from keep_alive import keep_alive
keep_alive()

import schedule
import time
from core.controller import is_bot_active
from core.signal_generator import generate_trade_signal
from core.reporter import send_daily_report

schedule.every().day.at("16:30").do(send_daily_report)
from core.log_backup import backup_logs

# Schedule daily backup
schedule.every().day.at("17:31").do(backup_logs)  # adjust time as needed

def run_bot():
    if is_bot_active():
        trade = generate_trade_signal()
        if trade:
            print(f"Trade signal sent: {trade['direction']} {trade['strike']} exp:{trade['expiration']}")
        else:
            print("No valid trade signal generated.")
    else:
        print("Bot is currently deactivated.")

if __name__ == "__main__":
    print("Starting SPY Options Bot...")
    while True:
        schedule.run_pending()
        run_bot()
        time.sleep(60)
import schedule
from core.reporter import send_daily_report

# Set daily time (24hr format)
schedule.every().day.at("17:30").do(send_daily_report)  # change time if needed

def run_bot():
    ...
    while True:
        schedule.run_pending()
        time.sleep(60)
