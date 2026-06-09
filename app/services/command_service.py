"""Remote command queue for client agents."""

from __future__ import annotations

from app.services.supabase_client import SupabaseClient
from app.auth.session import Session


ALLOWED_ACTIONS = (
    "revoke_license",
    "clear_revoke",
    "show_message",
    "collect_logs",
    "restart_agent",
    "tailscale_report",
)


class CommandService:
    def __init__(self):
        self._db = SupabaseClient()

    def list_commands(self, limit: int = 100) -> list:
        if not self._db.configured:
            return []
        return self._db.select(
            "commands",
            {"select": "*", "order": "created_at.desc", "limit": str(limit)},
        )

    def list_results(self, limit: int = 100) -> list:
        if not self._db.configured:
            return []
        return self._db.select(
            "command_results",
            {"select": "*", "order": "completed_at.desc", "limit": str(limit)},
        )

    def queue(self, machine_id: str, action: str, params: dict | None = None) -> dict:
        if action not in ALLOWED_ACTIONS:
            return {"success": False, "message": f"Action not allowed: {action}"}
        if not self._db.configured:
            return {"success": False, "message": "Supabase not configured."}
        actor = Session.username() or "admin"
        body = {
            "machine_id": machine_id,
            "action": action,
            "params": params or {},
            "actor": actor,
        }
        try:
            try:
                result = self._db.call_edge("admin_queue_command", body)
            except Exception:
                row = self._db.insert(
                    "commands",
                    {
                        "machine_id": machine_id,
                        "action": action,
                        "params": params or {},
                        "created_by": actor,
                        "status": "pending",
                    },
                )
                result = {"command_id": row.get("id")}
            return {"success": True, "message": "Command queued.", "data": result}
        except Exception as ex:
            return {"success": False, "message": str(ex)[:120]}
