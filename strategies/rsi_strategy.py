import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal():
    # Download SPY data (1h candles for 20 days)
    spy = yf.download("SPY", period="20d", interval="1h", progress=False)

    if spy.empty or len(spy) < 15:
        return None

    spy['RSI'] = calculate_rsi(spy)
    rsi_latest = spy['RSI'].iloc[-1]

    if pd.isna(rsi_latest):
        return None

    # Generate trade based on RSI
    if rsi_latest < 30:
        direction = "Call"
    elif rsi_latest > 70:
        direction = "Put"
    else:
        return None  # No signal

    current_price = spy['Close'].iloc[-1]
    strike = round(current_price)
    expiration = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    return {
        "direction": direction,
        "strike": strike,
        "expiration": expiration,
        "confidence": round(0.75 + abs(50 - rsi_latest) / 100, 2),
        "stop_loss": 0.2,
        "take_profit": 0.4,
        "strategy": "rsi_strategy"
    }
