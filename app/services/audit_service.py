"""Audit log service."""

from __future__ import annotations

from app.services.supabase_client import SupabaseClient


class AuditService:
    def __init__(self):
        self._db = SupabaseClient()

    def list_recent(self, limit: int = 100) -> list:
        if not self._db.configured:
            return []
        return self._db.select(
            "audit_log",
            {"select": "*", "order": "created_at.desc", "limit": str(limit)},
        )
