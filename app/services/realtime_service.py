"""Realtime polling service for Supabase tables (Flet-safe)."""

from __future__ import annotations

import threading
import time
from typing import Callable

from app.services.supabase_client import SupabaseClient
from app.utils.logger import logger

EventCallback = Callable[[str, dict], None]


class RealtimeService:
    """Polls Supabase for changes; invokes callbacks on the caller thread via page.run_thread."""

    def __init__(self, interval_sec: float = 2.0):
        self._db = SupabaseClient()
        self._interval = interval_sec
        self._callbacks: list[EventCallback] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_cmd_ts = ""
        self._last_result_ts = ""
        self._last_inst_ts = ""
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected and self._db.configured

    def subscribe(self, callback: EventCallback) -> None:
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unsubscribe(self, callback: EventCallback) -> None:
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _emit(self, event_type: str, payload: dict) -> None:
        for cb in list(self._callbacks):
            try:
                cb(event_type, payload)
            except Exception as ex:
                logger.debug("Realtime callback error: %s", ex)

    def _loop(self) -> None:
        while not self._stop.is_set():
            if not self._db.configured:
                self._connected = False
                time.sleep(self._interval)
                continue
            try:
                self._poll_commands()
                self._poll_results()
                self._poll_installations()
                self._connected = True
            except Exception as ex:
                self._connected = False
                logger.debug("Realtime poll error: %s", ex)
            time.sleep(self._interval)

    def _poll_commands(self) -> None:
        params = {"select": "*", "order": "created_at.desc", "limit": "5"}
        if self._last_cmd_ts:
            params["created_at"] = f"gt.{self._last_cmd_ts}"
        rows = self._db.select("commands", params if self._last_cmd_ts else {"select": "*", "order": "created_at.desc", "limit": "1"})
        if not rows:
            return
        newest = rows[0].get("created_at", "")
        if newest and newest != self._last_cmd_ts:
            if self._last_cmd_ts:
                for row in reversed(rows):
                    self._emit("command", row)
            self._last_cmd_ts = newest

    def _poll_results(self) -> None:
        rows = self._db.select(
            "command_results",
            {"select": "*", "order": "completed_at.desc", "limit": "1"},
        )
        if not rows:
            return
        newest = rows[0].get("completed_at", "")
        if newest and newest != self._last_result_ts:
            if self._last_result_ts:
                self._emit("command_result", rows[0])
            self._last_result_ts = newest

    def _poll_installations(self) -> None:
        rows = self._db.select(
            "installations",
            {"select": "*", "order": "updated_at.desc", "limit": "1"},
        )
        if not rows:
            return
        newest = rows[0].get("updated_at", "")
        if newest and newest != self._last_inst_ts:
            if self._last_inst_ts:
                self._emit("installation", rows[0])
            self._last_inst_ts = newest

    def ping(self) -> tuple[bool, str]:
        if not self._db.configured:
            return False, "Not configured"
        ok, msg = self._db.test_connection()
        if ok:
            self._connected = True
            return True, "Connected (polling active)"
        self._connected = False
        return False, msg
