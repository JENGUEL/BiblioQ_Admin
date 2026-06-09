"""Installation telemetry queries."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.services.supabase_client import SupabaseClient


class InstallationService:
    def __init__(self):
        self._db = SupabaseClient()

    def list_all(self, limit: int = 200) -> list:
        if not self._db.configured:
            return []
        return self._db.select(
            "installations",
            {
                "select": "*",
                "order": "last_seen_at.desc",
                "limit": str(limit),
            },
        )

    def get_stats(self) -> dict:
        rows = self.list_all(limit=500)
        now = datetime.now(timezone.utc)
        active_cutoff = now - timedelta(minutes=15)
        total = len(rows)
        active = 0
        revoked = 0
        for r in rows:
            if r.get("status") == "revoked":
                revoked += 1
            try:
                seen = datetime.fromisoformat(
                    r.get("last_seen_at", "").replace("Z", "+00:00")
                )
                if seen >= active_cutoff and r.get("status") != "revoked":
                    active += 1
            except Exception:
                pass
        return {
            "total": total,
            "active": active,
            "revoked": revoked,
            "offline": max(0, total - active - revoked),
        }

    def get_by_machine(self, machine_id: str) -> dict | None:
        rows = self._db.select(
            "installations",
            {"select": "*", "machine_id": f"eq.{machine_id}", "limit": "1"},
        )
        return rows[0] if rows else None
