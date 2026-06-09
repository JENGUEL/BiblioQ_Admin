#!/usr/bin/env python3
"""Create %LOCALAPPDATA%\\BiblioQ\\agent\\config.json from admin settings."""

from __future__ import annotations

import argparse
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from agent.machine import get_machine_id
from app.services.agent_setup import write_agent_config


def main() -> int:
    parser = argparse.ArgumentParser(description="Write BiblioQ agent config.json")
    parser.add_argument("--url", help="Supabase project URL (overrides admin config)")
    parser.add_argument("--agent-key", help="Agent API key (overrides admin config)")
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Check-in interval in seconds (default 300)",
    )
    args = parser.parse_args()

    try:
        path = write_agent_config(args.url, args.agent_key, args.interval)
    except ValueError as ex:
        print(f"Error: {ex}", file=sys.stderr)
        return 1

    print(f"Agent config written: {path}")
    print(f"Machine ID: {get_machine_id()}")
    print("Run: python agent/agent.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
