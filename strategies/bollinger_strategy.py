import yfinance as yf
import pandas as pd
from datetime import datetime

def run():
    print("[STRATEGY] Running Bollinger Bands Strategy...")
    try:
        data = yf.download("SPY", period="60d", interval="1d", progress=False)

        data["SMA_20"] = data["Close"].rolling(window=20).mean()
        data["STD_20"] = data["Close"].rolling(window=20).std()
        data["Upper"] = data["SMA_20"] + 2 * data["STD_20"]
        data["Lower"] = data["SMA_20"] - 2 * data["STD_20"]

        latest = data.iloc[-1]

        if latest["Close"] > latest["Upper"]:
            direction = "Put"
        elif latest["Close"] < latest["Lower"]:
            direction = "Call"
        else:
            return None

        expiration = (datetime.now() + pd.Timedelta(days=7)).strftime("%Y-%m-%d")
        strike = round(latest["Close"])

        signal = {
            "direction": direction,
            "strike": strike,
            "expiration": expiration,
            "confidence": 0.75,
            "stop_loss": 0.2,
            "take_profit": 0.4,
            "strategy": "bollinger_strategy",
        }
        print(f"[STRATEGY] ✅ Signal: {direction} {strike} exp:{expiration}")
        return signal

    except Exception as e:
        print(f"[STRATEGY ERROR] Bollinger Strategy failed: {e}")
        return None
