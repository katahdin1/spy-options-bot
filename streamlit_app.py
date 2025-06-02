import streamlit as st
from core.controller import is_bot_active, set_bot_state
from core.signal_generator import generate_trade_signal
from core.reporter import send_daily_report
import json
import os
import pandas as pd
from datetime import datetime

STATS_PATH = "data/strategy_stats.json"
HISTORY_PATH = "data/trade_history.csv"

st.set_page_config(page_title="📊 SPY Bot Dashboard", layout="centered")
st.title("🤖 SPY Options Bot Control Panel")

# --- BOT STATUS ---
st.subheader("🚦 Bot Status")
bot_status = is_bot_active()
status_text = "🟢 Active" if bot_status else "🔴 Inactive"
st.markdown(f"**Current Status:** {status_text}")

if st.button("🔄 Toggle Bot"):
    set_bot_state(not bot_status)
    st.experimental_rerun()

# --- MANUAL SIGNAL ---
st.subheader("⚡ Run Signal Generator")
if st.button("📡 Generate Signal Now"):
    signal = generate_trade_signal()
    if signal:
        st.success(f"Signal: {signal['direction']} {signal['strike']} (Conf: {signal['confidence']})")
    else:
        st.warning("No valid signal returned.")

# --- STRATEGY STATS ---
st.subheader("📈 Strategy Effectiveness")
if os.path.exists(STATS_PATH):
    with open(STATS_PATH) as f:
        stats = json.load(f)

    for strategy, data in stats.items():
        avg_conf = data["conf_sum"] / max(data["count"], 1)
        win_rate = data["est_wins"] / max(data["count"], 1)
        st.markdown(f"""
        **{strategy}**
        - Trades: `{data['count']}`
        - Wins (est): `{data['est_wins']}`
        - Avg Conf: `{avg_conf:.2f}`
        - Win Rate (est): `{win_rate:.1%}`
        """)
else:
    st.warning("No strategy stats yet.")

# --- TRADE HISTORY PREVIEW ---
st.subheader("📜 Trade History")
if os.path.exists(HISTORY_PATH):
    df = pd.read_csv(HISTORY_PATH)
    df['confidence'] = df['confidence'].astype(float).round(2)
    df = df.sort_values("timestamp", ascending=False)
    st.dataframe(df.head(15))
else:
    st.info("No trade history yet.")

# --- REPORT ---
st.subheader("📤 Send Daily Report")
if st.button("📧 Send Report Now"):
    send_daily_report()
    st.success("Report sent to email + Discord (if enabled).")
