"""Dashboard overview page."""

import flet as ft
from app import theme as T
from app.ui.components.stat_card import StatCard
from app.ui.components.data_table import build_table
from app.services.installation_service import InstallationService
from app.services.crash_service import CrashService
from app.services.command_service import CommandService


class DashboardPage:
    def __init__(self, page: ft.Page, realtime=None):
        self.page = page
        self.realtime = realtime
        self._stats_row = ft.Row(spacing=12)
        self._recent_table = ft.Container()
        self._activity = ft.Column(spacing=6)

    def build(self) -> ft.Control:
        self.refresh()
        return ft.Column(
            [
                T.page_title("Dashboard"),
                ft.Container(height=8),
                self._stats_row,
                ft.Container(height=16),
                ft.Text("Recently seen installations", size=14, font_family=T.FONT, color=T.C_MUTED),
                self._recent_table,
                ft.Container(height=16),
                ft.Text("Recent activity", size=14, font_family=T.FONT, color=T.C_MUTED),
                T.panel_container(self._activity, padding=12),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def on_realtime(self, event_type: str, payload: dict):
        if event_type == "command":
            self._prepend_activity(
                f"Command queued: {payload.get('action')} → {payload.get('machine_id', '')[:12]}"
            )
        elif event_type == "command_result":
            self._prepend_activity(
                f"Command {payload.get('status')}: {payload.get('output', '')[:80]}"
            )

    def _prepend_activity(self, text: str):
        self._activity.controls.insert(
            0,
            ft.Text(text, size=11, color=T.C_TEXT, font_family=T.FONT),
        )
        if len(self._activity.controls) > 12:
            self._activity.controls.pop()
        try:
            self._activity.update()
        except Exception:
            pass

    def refresh(self):
        inst = InstallationService()
        crash = CrashService()
        stats = inst.get_stats()
        crashes_7d = crash.count_last_days(7)
        cards = [
            StatCard("Total installs", str(stats["total"]), T.C_NEON_CYAN).build(),
            StatCard("Active (15 min)", str(stats["active"]), T.C_NEON_GREEN).build(),
            StatCard("Revoked", str(stats["revoked"]), T.C_NEON_MAGENTA).build(),
            StatCard("Crashes (7d)", str(crashes_7d), T.C_NEON_CYAN).build(),
        ]
        self._stats_row.controls = cards

        rows = inst.list_all(limit=10)
        table_rows = [
            [
                r.get("hostname", ""),
                (r.get("machine_id", "") or "")[:12],
                r.get("biblioq_version", ""),
                (r.get("status", "") or "").upper(),
                (r.get("last_seen_at", "") or "")[:19],
            ]
            for r in rows
        ]
        self._recent_table.content = build_table(
            ["Hostname", "Machine ID", "Version", "Status", "Last seen"],
            table_rows or [["No data yet", "", "", "", ""]],
        )

        cmds = CommandService().list_commands(limit=8)
        self._activity.controls.clear()
        for c in cmds:
            self._activity.controls.append(
                ft.Text(
                    f"{(c.get('created_at') or '')[:19]} — {c.get('action')} @ {c.get('machine_id', '')[:12]} ({c.get('status')})",
                    size=11,
                    color=T.C_MUTED,
                    font_family=T.FONT,
                )
            )
        if not self._activity.controls:
            self._activity.controls.append(
                ft.Text("No recent commands.", size=11, color=T.C_MUTED, font_family=T.FONT)
            )
