import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def generate_signal():
    print("[STRATEGY] Running Moving Average Crossover Strategy...")

    spy = yf.download("SPY", period="20d", interval="1h", progress=False)

    if spy.empty or len(spy) < 35:
        print("[STRATEGY] Not enough data.")
        return None

    spy = spy.copy()

    spy["SMA_10"] = spy["Close"].rolling(window=10).mean()
    spy["SMA_30"] = spy["Close"].rolling(window=30).mean()

    if "SMA_10" not in spy.columns or "SMA_30" not in spy.columns or len(spy) < 2:
        print("[STRATEGY] MAs not ready.")
        return None

    prev = spy.iloc[-2]
    latest = spy.iloc[-1]

    try:
        sma10_prev = prev["SMA_10"].item()
        sma30_prev = prev["SMA_30"].item()
        sma10_now = latest["SMA_10"].item()
        sma30_now = latest["SMA_30"].item()
        strike = round(latest["Close"].item())

    except Exception as e:
        print(f"[STRATEGY] SMA conversion error: {e}")
        return None

    bullish = sma10_prev < sma30_prev and sma10_now > sma30_now
    bearish = sma10_prev > sma30_prev and sma10_now < sma30_now

    if not bullish and not bearish:
        print("[STRATEGY] No crossover.")
        return None

    direction = "Call" if bullish else "Put"
    strike = round(latest["Close"].item())

    expiration = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    print(f"[STRATEGY] ✅ Signal: {direction} {strike} exp:{expiration}")

    return {
        "direction": direction,
        "strike": strike,
        "expiration": expiration,
        "confidence": 0.82,
        "stop_loss": 0.2,
        "take_profit": 0.4,
        "strategy": "moving_avg_strategy"
    }
