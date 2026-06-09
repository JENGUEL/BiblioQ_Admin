"""BiblioQ background agent main loop."""

from __future__ import annotations

import json
import os
import socket
import sys
import time

import requests

AGENT_VERSION = "1.0.0"

# Allow running from repo root or frozen install dir
if getattr(sys, "frozen", False):
    _ROOT = os.path.dirname(sys.executable)
    _pkg_root = os.path.dirname(_ROOT) if os.path.basename(_ROOT).lower() == "agent" else _ROOT
else:
    _ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _pkg_root = _ROOT
for p in (_ROOT, _pkg_root):
    if p and p not in sys.path:
        sys.path.insert(0, p)

from agent.config import load_config
from agent.machine import get_machine_id, get_hostname, get_os_version
from agent.commands.handlers import dispatch

BIBLIOQ_DATA = os.path.join(os.path.expanduser("~"), "AppData", "Local", "BiblioQ", "data")
LICENSE_FILE = os.path.join(BIBLIOQ_DATA, ".license")
CRASH_DIR = os.path.join(BIBLIOQ_DATA, "crashes")


def _normalize_base_url(raw: str) -> str:
    url = (raw or "").strip().rstrip("/")
    if url.endswith("/rest/v1"):
        url = url[: -len("/rest/v1")].rstrip("/")
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url.lstrip("/")
    return url


def _local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return ""


def _read_license_key() -> str:
    if not os.path.isfile(LICENSE_FILE):
        return ""
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("license_key", "")
    except Exception:
        return ""


def _read_biblioq_version() -> str:
    state = os.path.join(BIBLIOQ_DATA, "agent_state.json")
    if os.path.isfile(state):
        try:
            with open(state, "r", encoding="utf-8") as f:
                return json.load(f).get("biblioq_version", "")
        except Exception:
            pass
    return ""


def _biblioq_running() -> bool:
    state = os.path.join(BIBLIOQ_DATA, "agent_state.json")
    if os.path.isfile(state):
        try:
            with open(state, "r", encoding="utf-8") as f:
                return bool(json.load(f).get("biblioq_running", False))
        except Exception:
            pass
    return False


def build_payload() -> dict:
    return {
        "machine_id": get_machine_id(),
        "hostname": get_hostname(),
        "os_version": get_os_version(),
        "biblioq_version": _read_biblioq_version(),
        "license_key": _read_license_key(),
        "ip": _local_ip(),
        "agent_version": AGENT_VERSION,
        "biblioq_running": _biblioq_running(),
    }


def _edge_post(cfg: dict, function_name: str, body: dict) -> dict:
    base = _normalize_base_url(cfg.get("supabase_url") or "")
    if not base:
        print("Check-in failed: supabase_url not configured.")
        return {}

    url = f"{base}/functions/v1/{function_name}"
    headers = {"Content-Type": "application/json"}
    key = cfg.get("agent_api_key") or ""
    if not key:
        print(f"{function_name} failed: agent_api_key not configured.")
        return {}
    headers["x-agent-key"] = key

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code == 401:
            print(f"{function_name} failed: unauthorized (check AGENT_API_KEY).")
            return {}
        if resp.status_code == 404:
            print(
                f"{function_name} failed: function not deployed on Supabase. "
                f"Deploy it in Dashboard → Edge Functions or run: "
                f"supabase functions deploy {function_name}"
            )
            return {}
        resp.raise_for_status()
        return resp.json() if resp.text else {}
    except Exception as ex:
        print(f"{function_name} failed: {ex}")
        return {}


def checkin(cfg: dict) -> dict:
    fn = cfg.get("edge_function") or "agent_checkin"
    return _edge_post(cfg, fn, build_payload())


def report_result(cfg: dict, command_id: str, status: str, output: str) -> None:
    _edge_post(
        cfg,
        "agent_command_result",
        {
            "payload": {
                "command_id": command_id,
                "machine_id": get_machine_id(),
                "status": status,
                "output": output,
            }
        },
    )


def upload_crashes(cfg: dict) -> None:
    if not os.path.isdir(CRASH_DIR):
        return
    for name in os.listdir(CRASH_DIR):
        if not name.endswith(".json"):
            continue
        path = os.path.join(CRASH_DIR, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            result = _edge_post(
                cfg,
                "agent_crash_report",
                {
                    "machine_id": get_machine_id(),
                    "app_version": data.get("app_version", ""),
                    "error_type": data.get("error_type", "Error"),
                    "stack_trace": data.get("stack_trace", ""),
                    "occurred_at": data.get("occurred_at"),
                },
            )
            if result.get("ok"):
                os.remove(path)
        except Exception as ex:
            print(f"Crash upload failed for {name}: {ex}")


def run_once(cfg: dict) -> None:
    result = checkin(cfg)
    upload_crashes(cfg)
    for cmd in result.get("pending_commands") or []:
        cid = cmd.get("command_id")
        action = cmd.get("action")
        params = cmd.get("params") or {}
        ok, output = dispatch(action, params)
        if cid:
            report_result(cfg, cid, "success" if ok else "failed", output)
        if action == "restart_agent" and ok:
            raise SystemExit(0)


def main_loop():
    cfg = load_config()
    interval = int(cfg.get("checkin_interval_sec") or 300)
    print(f"BiblioQ Agent started. Interval={interval}s machine={get_machine_id()}")
    while True:
        run_once(cfg)
        time.sleep(interval)


if __name__ == "__main__":
    main_loop()
