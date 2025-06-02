import csv
import os
from datetime import datetime
from notifier.emailer import send_email
from notifier.discord import send_discord_alert

TRADE_HISTORY_PATH = "data/trade_history.csv"

def send_daily_report():
    try:
        today = datetime.now().strftime("%Y-%m-%d")

        if not os.path.exists(TRADE_HISTORY_PATH):
            print("[REPORT] No trade history found.")
            return

        with open(TRADE_HISTORY_PATH, "r") as file:
            reader = csv.DictReader(file)
            today_trades = [row for row in reader if row["date"] == today]

        if not today_trades:
            print("[REPORT] No trades found for today.")
            return

        report_lines = []
        strategy_summary = {}

        for trade in today_trades:
            line = (
                f"- {trade['direction']} ${trade['strike']} exp:{trade['expiration']} | "
                f"Conf: {round(float(trade['confidence']) * 100)}% | "
                f"SL: {trade['stop_loss']} | TP: {trade['take_profit']} | "
                f"Strategy: {trade['strategy']}"
            )
            report_lines.append(line)

            strategy = trade["strategy"]
            strategy_summary[strategy] = strategy_summary.get(strategy, 0) + 1

        summary_block = "\n".join(report_lines)
        strat_block = "\n".join(
            f"• {name}: {count} trade(s)" for name, count in strategy_summary.items()
        )

        final_report = (
            f"📊 **SPY Options Bot – Daily Report ({today})**\n\n"
            f"🧾 **Trades Executed Today:**\n{summary_block}\n\n"
            f"📈 **Strategy Breakdown:**\n{strat_block}"
        )

        send_email(subject="📊 SPY Bot Daily Report", body=final_report)
        send_discord_alert({"content": final_report})
        print("[REPORT] ✅ Daily report sent.")

    except Exception as e:
        print(f"[REPORT ERROR] Failed to generate or send report: {e}")
