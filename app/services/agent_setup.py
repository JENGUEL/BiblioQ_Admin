"""Write BiblioQ agent config.json on the local machine."""

from __future__ import annotations

import os
import sys

from app.config import load_config, CONFIG_FILE
from app.utils.crypto import decrypt_config_value
from app.utils.supabase_url import normalize_supabase_url

# Import agent path helpers from sibling package
_AGENT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _AGENT_ROOT not in sys.path:
    sys.path.insert(0, _AGENT_ROOT)

from agent.config import (  # noqa: E402
    get_agent_config_paths,
    get_primary_agent_config_file,
    save_config as save_agent_config,
)


def write_agent_config(
    supabase_url: str | None = None,
    agent_api_key: str | None = None,
    checkin_interval_sec: int = 300,
) -> str:
    """Write agent config.json. Uses admin saved config when args omitted."""
    url = supabase_url
    key = agent_api_key

    if not url or not key:
        if not os.path.isfile(CONFIG_FILE):
            raise ValueError(
                "Admin settings not saved. Fill Supabase URL and Agent API key first."
            )
        cfg = load_config()
        if not url:
            url = cfg.get("supabase_url") or ""
        if not key:
            key = decrypt_config_value(cfg.get("agent_api_key") or "")

    url = normalize_supabase_url(url)
    key = (key or "").strip()
    if not key:
        raise ValueError("Agent API key is required.")

    return save_agent_config(
        {
            "supabase_url": url,
            "agent_api_key": key,
            "checkin_interval_sec": checkin_interval_sec,
            "edge_function": "agent_checkin",
        },
        mirror_user=True,
    )


AGENT_CONFIG_DIR = os.path.dirname(get_primary_agent_config_file())
AGENT_CONFIG_FILE = get_primary_agent_config_file()
