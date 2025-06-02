import os
import json
import csv
import importlib
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv
import yaml

# Paths
SETTINGS_PATH = "config/settings.yaml"
TRADE_HISTORY_PATH = "data/trade_history.json"
TRADE_HISTORY_CSV = "data/trade_history.csv"
STRATEGY_STATS_PATH = "data/strategy_stats.json"

load_dotenv()

def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[CONFIG ERROR] Failed to load settings.yaml: {e}")
        return {}

def get_strategies():
    config = load_settings()
    enabled_strategies = config.get("strategies", {}).get("enabled", [])
    strategies = []
    for name in enabled_strategies:
        try:
            module_path = f"strategies.{name}"
            strategy_module = importlib.import_module(module_path)
            strategies.append(strategy_module)
        except Exception as e:
            print(f"[IMPORT ERROR] Failed to import strategy {name}: {e}")
    return strategies

def log_trade(trade_data):
    timestamp = datetime.now().isoformat()
    trade_data["timestamp"] = timestamp

    # Log to JSON
    try:
        os.makedirs(os.path.dirname(TRADE_HISTORY_PATH), exist_ok=True)
        if os.path.exists(TRADE_HISTORY_PATH):
            with open(TRADE_HISTORY_PATH, "r") as f:
                history = json.load(f)
        else:
            history = []
        history.append(trade_data)
        with open(TRADE_HISTORY_PATH, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"[LOG ERROR] Failed to log trade to JSON: {e}")

    # Log to CSV
    try:
        os.makedirs(os.path.dirname(TRADE_HISTORY_CSV), exist_ok=True)
        file_exists = os.path.isfile(TRADE_HISTORY_CSV)
        with open(TRADE_HISTORY_CSV, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "timestamp", "direction", "strike", "expiration",
                "confidence", "stop_loss", "take_profit", "strategy"
            ])
            if not file_exists:
                writer.writeheader()
            writer.writerow(trade_data)
    except Exception as e:
        print(f"[LOG ERROR] Failed to log trade to CSV: {e}")

def update_strategy_stats(trade):
    try:
        os.makedirs(os.path.dirname(STRATEGY_STATS_PATH), exist_ok=True)
        if os.path.exists(STRATEGY_STATS_PATH):
            with open(STRATEGY_STATS_PATH, "r") as f:
                stats = json.load(f)
        else:
            stats = {}

        strat = trade["strategy"]
        conf = trade["confidence"]
        ts = trade["timestamp"]

        if strat not in stats:
            stats[strat] = {
                "count": 0,
                "est_wins": 0,
                "conf_sum": 0.0,
                "last_used": None
            }

        stats[strat]["count"] += 1
        stats[strat]["conf_sum"] += conf
        stats[strat]["last_used"] = ts
        if conf >= 0.6:
            stats[strat]["est_wins"] += 1

        with open(STRATEGY_STATS_PATH, "w") as f:
            json.dump(stats, f, indent=2)

    except Exception as e:
        print(f"[STATS ERROR] Failed to update strategy stats: {e}")

def generate_trade_signal():
    config = load_settings()
    enabled_strategies = config.get("strategies", {}).get("enabled", [])
    weights = config.get("strategies", {}).get("weights", {})
    strategies = get_strategies()

    signals = []

    for strategy in strategies:
        try:
            signal = strategy.run()
            if signal:
                signals.append(signal)
                print(f"[SIGNAL] Strategy {strategy.__module__} returned: {signal}")
            else:
                print(f"[SIGNAL WARNING] Invalid or empty signal from {strategy.__module__}")
        except Exception as e:
            print(f"[SIGNAL ERROR] {strategy.__module__} failed: {e}")

    if not signals:
        print("[SIGNAL] ❌ No valid signals from any strategy.")
        return None

    # Weighted vote
    scores = defaultdict(float)
    weighted_signals = defaultdict(list)

    for s in signals:
        direction = s["direction"]
        weight = weights.get(s["strategy"], 1.0)
        score = s["confidence"] * weight
        scores[direction] += score
        weighted_signals[direction].append((s, score))

    best_direction = max(scores, key=scores.get)
    best_signal = max(weighted_signals[best_direction], key=lambda x: x[1])[0]

    print(f"[SIGNAL] ✅ Consensus signal: {best_signal}")
    log_trade(best_signal)
    update_strategy_stats(best_signal)
    return best_signal
