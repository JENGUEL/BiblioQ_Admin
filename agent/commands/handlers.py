"""Command handlers executed locally by the agent."""

import json
import os
from datetime import datetime, timezone

BIBLIOQ_DATA = os.path.join(os.path.expanduser("~"), "AppData", "Local", "BiblioQ", "data")
REVOKED_FILE = os.path.join(BIBLIOQ_DATA, "license_revoked.json")
MESSAGE_FILE = os.path.join(BIBLIOQ_DATA, "pending_message.json")
STATE_FILE = os.path.join(BIBLIOQ_DATA, "agent_state.json")


def _ensure_data():
    os.makedirs(BIBLIOQ_DATA, exist_ok=True)


def handle_clear_revoke(params: dict) -> str:
    _ensure_data()
    if os.path.isfile(REVOKED_FILE):
        os.remove(REVOKED_FILE)
        return "License revoke flag cleared."
    return "No revoke flag present."


def handle_revoke_license(params: dict) -> str:
    _ensure_data()
    payload = {
        "revoked": True,
        "message": params.get("message", "License revoked by administrator."),
        "revoked_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(REVOKED_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return "License revoke flag written."


def handle_show_message(params: dict) -> str:
    _ensure_data()
    payload = {
        "message": params.get("message", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(MESSAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return "Message queued for BiblioQ."


def handle_restart_agent(params: dict) -> str:
    return "Restart requested (exit and service will relaunch)."


def handle_collect_logs(params: dict) -> str:
    return "Log collection queued (upload via Supabase Storage in Phase 3)."


def handle_tailscale_report(params: dict) -> str:
    return "Tailscale reporting deferred to Phase 5."


HANDLERS = {
    "revoke_license": handle_revoke_license,
    "clear_revoke": handle_clear_revoke,
    "show_message": handle_show_message,
    "restart_agent": handle_restart_agent,
    "collect_logs": handle_collect_logs,
    "tailscale_report": handle_tailscale_report,
}


def dispatch(action: str, params: dict) -> tuple[bool, str]:
    fn = HANDLERS.get(action)
    if not fn:
        return False, f"Unknown action: {action}"
    try:
        return True, fn(params or {})
    except Exception as ex:
        return False, str(ex)[:200]
