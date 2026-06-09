"""Track remote command progress with live polling."""

from __future__ import annotations

import threading
import time

from app.services.supabase_client import SupabaseClient


class CommandTracker:
    STEPS = ("Queued", "Pending on agent", "Completed")

    def __init__(self, command_id: str | None, machine_id: str, action: str):
        self.command_id = command_id
        self.machine_id = machine_id
        self.action = action
        self.status = "queued"
        self.output = ""
        self.step_index = 0
        self._db = SupabaseClient()
        self._done = False

    def poll_until_done(self, callback, timeout_sec: float = 90.0, interval: float = 1.5) -> None:
        """Poll command status; callback(tracker) on each update. Runs in background thread."""

        def _run():
            deadline = time.time() + timeout_sec
            while time.time() < deadline and not self._done:
                self._refresh()
                callback(self)
                if self._done:
                    return
                time.sleep(interval)
            if not self._done:
                self.status = "timeout"
                self.output = "Agent did not respond in time. Check agent is running on the PC."
                callback(self)

        threading.Thread(target=_run, daemon=True).start()

    def _refresh(self) -> None:
        if not self._db.configured or not self.command_id:
            return
        try:
            rows = self._db.select(
                "commands",
                {"select": "*", "id": f"eq.{self.command_id}"},
            )
            if rows:
                cmd = rows[0]
                st = (cmd.get("status") or "pending").lower()
                if st in ("sent", "acked"):
                    self.step_index = 1
                    self.status = st
                elif st in ("failed", "cancelled"):
                    self._done = True
                    self.status = st
                self._load_result()
                if self.output:
                    self.step_index = 2
                    self._done = True
                    self.status = "success"
        except Exception:
            pass

    def _load_result(self) -> None:
        if not self.command_id:
            return
        try:
            rows = self._db.select(
                "command_results",
                {"select": "*", "command_id": f"eq.{self.command_id}", "limit": "1"},
            )
            if rows:
                self.output = rows[0].get("output", "")
                self.status = rows[0].get("status", self.status)
                self._done = True
                self.step_index = 2
        except Exception:
            pass

    @staticmethod
    def from_response(action: str, machine_id: str, result: dict) -> "CommandTracker":
        cmd_id = None
        payload = result
        if isinstance(result, dict) and "data" in result:
            payload = result.get("data") or {}
        if isinstance(payload, dict):
            cmd_id = payload.get("command_id")
        return CommandTracker(cmd_id, machine_id, action)
