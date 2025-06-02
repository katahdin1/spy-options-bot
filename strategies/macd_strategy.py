import yfinance as yf
import pandas as pd
from datetime import datetime

def run():
    print("[STRATEGY] Running MACD Strategy...")
    try:
        data = yf.download("SPY", period="60d", interval="1d", progress=False)

        data["EMA_12"] = data["Close"].ewm(span=12, adjust=False).mean()
        data["EMA_26"] = data["Close"].ewm(span=26, adjust=False).mean()
        data["MACD"] = data["EMA_12"] - data["EMA_26"]
        data["Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()

        latest = data.iloc[-1]
        prev = data.iloc[-2]

        if prev["MACD"] < prev["Signal"] and latest["MACD"] > latest["Signal"]:
            direction = "Call"
        elif prev["MACD"] > prev["Signal"] and latest["MACD"] < latest["Signal"]:
            direction = "Put"
        else:
            return None

        expiration = (datetime.now() + pd.Timedelta(days=7)).strftime("%Y-%m-%d")
        strike = round(latest["Close"])

        signal = {
            "direction": direction,
            "strike": strike,
            "expiration": expiration,
            "confidence": 0.76,
            "stop_loss": 0.2,
            "take_profit": 0.4,
            "strategy": "macd_strategy",
        }
        print(f"[STRATEGY] ✅ Signal: {direction} {strike} exp:{expiration}")
        return signal

    except Exception as e:
        print(f"[STRATEGY ERROR] MACD Strategy failed: {e}")
        return None
