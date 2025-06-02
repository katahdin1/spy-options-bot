import yaml
import os

SETTINGS_PATH = "config/settings.yaml"


def load_config():
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"[CONFIG ERROR] settings.yaml not found at: {SETTINGS_PATH}")
            return {}

        with open(SETTINGS_PATH, "r") as f:
            config = yaml.safe_load(f) or {}
            return config
    except yaml.YAMLError as ye:
        print(f"[CONFIG ERROR] YAML parsing failed: {ye}")
    except Exception as e:
        print(f"[CONFIG ERROR] Failed to load config: {e}")
    return {}


def save_config(config):
    try:
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, "w") as f:
            yaml.safe_dump(config, f)
        print("[CONFIG] settings.yaml saved.")
    except Exception as e:
        print(f"[CONFIG ERROR] Failed to save config: {e}")


def is_bot_active():
    config = load_config()
    try:
        return config.get("bot", {}).get("active", False)
    except Exception as e:
        print(f"[CONFIG ERROR] Unable to determine bot status: {e}")
        return False


def set_bot_state(state: bool):
    config = load_config()
    try:
        config.setdefault("bot", {})["active"] = state
        save_config(config)
        print(f"[CONTROL] Bot {'activated' if state else 'deactivated'}.")
    except Exception as e:
        print(f"[CONTROL ERROR] Failed to update bot state: {e}")
