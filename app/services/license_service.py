"""License revoke and management."""

from __future__ import annotations

from app.services.supabase_client import SupabaseClient
from app.auth.session import Session


class LicenseAdminService:
    def __init__(self):
        self._db = SupabaseClient()

    def list_licenses(self, limit: int = 200) -> list:
        if not self._db.configured:
            return []
        return self._db.select(
            "licenses",
            {"select": "*", "order": "updated_at.desc", "limit": str(limit)},
        )

    def revoke(
        self, license_key: str, machine_id: str | None, message: str
    ) -> dict:
        if not self._db.configured:
            return {"success": False, "message": "Supabase not configured."}
        try:
            actor = Session.username() or "admin"
            try:
                result = self._db.call_edge(
                    "admin_revoke_license",
                    {
                        "license_key": license_key,
                        "machine_id": machine_id,
                        "message": message,
                        "actor": actor,
                    },
                )
            except Exception:
                result = self._db.rpc(
                    "admin_revoke_license",
                    {
                        "p_license_key": license_key,
                        "p_machine_id": machine_id,
                        "p_message": message,
                        "p_actor": actor,
                    },
                )
            return {"success": True, "message": "License revoked.", "data": result}
        except Exception as ex:
            return {"success": False, "message": str(ex)[:120]}

    def restore(
        self, license_key: str, machine_id: str | None
    ) -> dict:
        if not self._db.configured:
            return {"success": False, "message": "Supabase not configured."}
        try:
            actor = Session.username() or "admin"
            try:
                result = self._db.call_edge(
                    "admin_restore_license",
                    {
                        "license_key": license_key,
                        "machine_id": machine_id,
                        "actor": actor,
                    },
                )
            except Exception:
                result = self._db.rpc(
                    "admin_restore_license",
                    {
                        "p_license_key": license_key,
                        "p_machine_id": machine_id,
                        "p_actor": actor,
                    },
                )
            return {"success": True, "message": "License restored.", "data": result}
        except Exception as ex:
            return {"success": False, "message": str(ex)[:120]}
