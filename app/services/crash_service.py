"""Crash report aggregation."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.services.supabase_client import SupabaseClient


class CrashService:
    def __init__(self):
        self._db = SupabaseClient()

    def list_reports(self, limit: int = 200, unresolved_only: bool = False) -> list:
        if not self._db.configured:
            return []
        params = {
            "select": "*",
            "order": "occurred_at.desc",
            "limit": str(limit),
        }
        if unresolved_only:
            params["resolved"] = "eq.false"
        return self._db.select("crash_reports", params)

    def count_last_days(self, days: int = 7) -> int:
        rows = self.list_reports(limit=500)
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        count = 0
        for r in rows:
            try:
                t = datetime.fromisoformat(
                    r.get("occurred_at", "").replace("Z", "+00:00")
                )
                if t >= cutoff:
                    count += 1
            except Exception:
                pass
        return count

    def set_resolved(self, report_id: str, resolved: bool = True) -> dict:
        if not self._db.configured:
            return {"success": False, "message": "Supabase not configured."}
        try:
            self._db.update(
                "crash_reports",
                {"id": f"eq.{report_id}"},
                {"resolved": resolved},
            )
            return {"success": True, "message": "Updated."}
        except Exception as ex:
            return {"success": False, "message": str(ex)[:120]}
