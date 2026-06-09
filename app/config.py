"""Admin app configuration."""

import json
import os

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Local", "BiblioQ_Admin", "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "admin_config.json")

DEFAULT_CONFIG = {
    "supabase_url": "",
    "supabase_service_key": "",
    "supabase_anon_key": "",
    "admin_api_token": "",
    "agent_api_key": "",
    "edge_functions_base": "",
}


def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_config() -> dict:
    ensure_config_dir()
    if not os.path.isfile(CONFIG_FILE):
        return dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        out = dict(DEFAULT_CONFIG)
        out.update(data)
        return out
    except Exception:
        return dict(DEFAULT_CONFIG)


def save_config(data: dict) -> None:
    ensure_config_dir()
    merged = dict(DEFAULT_CONFIG)
    merged.update(data)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)


def is_configured() -> bool:
    cfg = load_config()
    return bool(cfg.get("supabase_url") and cfg.get("supabase_service_key"))
