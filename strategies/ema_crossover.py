import yfinance as yf
import pandas as pd
from datetime import datetime

def run():
    print("[STRATEGY] Running EMA Crossover Strategy...")
    try:
        data = yf.download("SPY", period="60d", interval="1d", progress=False)

        data["EMA_10"] = data["Close"].ewm(span=10, adjust=False).mean()
        data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()

        prev = data.iloc[-2]
        latest = data.iloc[-1]

        if prev["EMA_10"] < prev["EMA_20"] and latest["EMA_10"] > latest["EMA_20"]:
            direction = "Call"
        elif prev["EMA_10"] > prev["EMA_20"] and latest["EMA_10"] < latest["EMA_20"]:
            direction = "Put"
        else:
            return None

        expiration = (datetime.now() + pd.Timedelta(days=7)).strftime("%Y-%m-%d")
        strike = round(latest["Close"])

        signal = {
            "direction": direction,
            "strike": strike,
            "expiration": expiration,
            "confidence": 0.74,
            "stop_loss": 0.2,
            "take_profit": 0.4,
            "strategy": "ema_crossover",
        }
        print(f"[STRATEGY] ✅ Signal: {direction} {strike} exp:{expiration}")
        return signal

    except Exception as e:
        print(f"[STRATEGY ERROR] EMA Crossover Strategy failed: {e}")
        return None
