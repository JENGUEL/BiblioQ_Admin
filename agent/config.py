"""Agent configuration paths and load/save."""

from __future__ import annotations

import json
import os
import sys

APP_NAME = "BiblioQ"
DEFAULT = {
    "supabase_url": "",
    "agent_api_key": "",
    "checkin_interval_sec": 300,
    "edge_function": "agent_checkin",
}


def _programdata_agent_dir() -> str:
    program_data = os.environ.get("ProgramData", r"C:\ProgramData")
    return os.path.join(program_data, APP_NAME, "agent")


def _localappdata_agent_dir() -> str:
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    if local_appdata:
        return os.path.join(local_appdata, APP_NAME, "agent")
    return os.path.join(os.path.expanduser("~"), "AppData", "Local", APP_NAME, "agent")


def get_agent_config_dirs() -> list[str]:
    """Search order: machine-wide ProgramData, then per-user LocalAppData."""
    seen: set[str] = set()
    dirs: list[str] = []
    for path in (_programdata_agent_dir(), _localappdata_agent_dir()):
        norm = os.path.normcase(os.path.abspath(path))
        if norm not in seen:
            seen.add(norm)
            dirs.append(path)
    return dirs


def get_agent_config_paths() -> list[str]:
    return [os.path.join(d, "config.json") for d in get_agent_config_dirs()]


def get_primary_agent_config_dir() -> str:
    """Write target for installers and admin setup (service-readable)."""
    return _programdata_agent_dir()


def get_primary_agent_config_file() -> str:
    return os.path.join(get_primary_agent_config_dir(), "config.json")


def resolve_config_file() -> str | None:
    for path in get_agent_config_paths():
        if os.path.isfile(path):
            return path
    return None


def ensure_dir(path: str | None = None) -> str:
    target = path or get_primary_agent_config_dir()
    os.makedirs(target, exist_ok=True)
    return target


def load_config() -> dict:
    path = resolve_config_file()
    if not path:
        return dict(DEFAULT)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = dict(DEFAULT)
    out.update(data)
    return out


def save_config(data: dict, *, mirror_user: bool = True) -> str:
    """Save to ProgramData; optionally mirror to LocalAppData for dev runs."""
    merged = dict(DEFAULT)
    merged.update(data)
    primary_dir = ensure_dir(get_primary_agent_config_dir())
    primary_path = os.path.join(primary_dir, "config.json")
    with open(primary_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    if mirror_user:
        user_dir = ensure_dir(_localappdata_agent_dir())
        user_path = os.path.join(user_dir, "config.json")
        if os.path.normcase(user_path) != os.path.normcase(primary_path):
            with open(user_path, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=2)

    return primary_path


# Backward-compatible module constants
AGENT_DIR = get_primary_agent_config_dir()
CONFIG_FILE = get_primary_agent_config_file()
