"""Installations management page."""

from __future__ import annotations

import csv
import io
from datetime import datetime, timezone

import flet as ft
from app import theme as T
from app.ui.components.data_table import build_table
from app.services.installation_service import InstallationService
from app.services.license_service import LicenseAdminService
from app.services.command_service import CommandService
from app.services.command_tracker import CommandTracker


def _format_last_seen(iso: str) -> str:
    if not iso:
        return "Never"
    try:
        seen = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - seen
        mins = int(delta.total_seconds() / 60)
        if mins < 1:
            return "Just now"
        if mins < 60:
            return f"{mins}m ago"
        hours = mins // 60
        if hours < 48:
            return f"{hours}h ago"
        return iso[:19]
    except Exception:
        return iso[:19] if iso else "—"


def _online_dot(last_seen: str, status: str) -> str:
    if (status or "").lower() == "revoked":
        return "offline"
    try:
        seen = datetime.fromisoformat((last_seen or "").replace("Z", "+00:00"))
        mins = (datetime.now(timezone.utc) - seen).total_seconds() / 60
        return "online" if mins <= 15 else "offline"
    except Exception:
        return "offline"


class InstallationsPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self._table_host = ft.Container()
        self._rows_cache: list = []
        self._search = ft.TextField(
            label="Search hostname or machine ID",
            border_color=T.C_BORDER,
            color=T.C_TEXT,
            on_change=lambda e: self._apply_filter(),
        )
        self._status_filter = ft.Dropdown(
            label="Status",
            width=160,
            border_color=T.C_BORDER,
            options=[
                ft.dropdown.Option("all", "All"),
                ft.dropdown.Option("active", "Active"),
                ft.dropdown.Option("revoked", "Revoked"),
                ft.dropdown.Option("offline", "Offline"),
            ],
            value="all",
        )
        self._status_filter.on_select = lambda e: self._apply_filter()

    def build(self) -> ft.Control:
        self.refresh()
        self._render_table()
        return ft.Column(
            [
                ft.Row(
                    [
                        T.page_title("Installations"),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Export CSV",
                            style=T.neon_button_style(T.C_PANEL_ALT),
                            on_click=self._export_csv,
                        ),
                        ft.ElevatedButton(
                            "Refresh",
                            style=T.neon_button_style(),
                            on_click=lambda e: self._refresh_ui(),
                        ),
                    ],
                ),
                ft.Container(height=8),
                ft.Row([self._search, self._status_filter], spacing=12),
                ft.Container(height=8),
                self._table_host,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh(self):
        self._rows_cache = InstallationService().list_all()

    def _filtered_rows(self) -> list:
        q = (self._search.value or "").strip().lower()
        st = self._status_filter.value or "all"
        rows = self._rows_cache
        if q:
            rows = [
                r
                for r in rows
                if q in (r.get("hostname") or "").lower()
                or q in (r.get("machine_id") or "").lower()
            ]
        if st != "all":
            if st == "offline":
                rows = [r for r in rows if _online_dot(r.get("last_seen_at", ""), r.get("status", "")) == "offline"]
            else:
                rows = [r for r in rows if (r.get("status") or "").lower() == st]
        return rows

    def _apply_filter(self):
        self._render_table()
        self._table_host.update()

    def _refresh_ui(self):
        self.refresh()
        self._render_table()
        self._table_host.update()

    def _render_table(self):
        rows = self._filtered_rows()
        table_rows = []
        for r in rows:
            online = _online_dot(r.get("last_seen_at", ""), r.get("status", ""))
            dot = "●" if online == "online" else "○"
            table_rows.append(
                [
                    f"{dot} {r.get('hostname', '')}",
                    (r.get("machine_id", "") or "")[:16],
                    r.get("license_key", "") or "—",
                    r.get("biblioq_version", ""),
                    (r.get("status", "") or "").upper(),
                    _format_last_seen(r.get("last_seen_at", "")),
                ]
            )
        self._table_host.content = build_table(
            ["Host", "Machine ID", "License", "Version", "Status", "Last seen"],
            table_rows or [["No installations yet", "", "", "", "", ""]],
            on_row_click=self._row_action,
        )

    def _row_action(self, index: int):
        rows = self._filtered_rows()
        if index >= len(rows):
            return
        row = rows[index]
        is_revoked = (row.get("status") or "").lower() == "revoked"
        reason = ft.TextField(
            label="Revoke message",
            value="License revoked by administrator.",
            border_color=T.C_BORDER,
        )
        msg_field = ft.TextField(
            label="Message to show on BiblioQ",
            value="Message from administrator.",
            border_color=T.C_BORDER,
        )
        tracker_text = ft.Text("", size=11, color=T.C_MUTED, font_family=T.FONT)

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=T.C_PANEL,
            title=ft.Text(f"Actions: {row.get('hostname')}", color=T.C_TEXT, font_family=T.FONT),
            content=ft.Column(
                [
                    ft.Text(f"Machine: {row.get('machine_id', '')}", size=11, color=T.C_MUTED),
                    reason,
                    msg_field,
                    tracker_text,
                ],
                height=220,
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self._close_dlg(dlg)),
                ft.TextButton(
                    "Restart agent",
                    on_click=lambda e: self._quick_cmd(row, "restart_agent", {}, dlg, tracker_text),
                ),
                ft.TextButton(
                    "Send message",
                    on_click=lambda e: self._quick_cmd(
                        row, "show_message", {"message": msg_field.value or ""}, dlg, tracker_text
                    ),
                ),
                ft.TextButton(
                    "Restore license" if is_revoked else "Revoke license",
                    on_click=lambda e: (
                        self._restore(row, dlg, tracker_text)
                        if is_revoked
                        else self._revoke(row, reason.value, dlg, tracker_text)
                    ),
                ),
            ],
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def _track(self, action: str, row: dict, result: dict, tracker_text: ft.Text):
        tracker = CommandTracker.from_response(action, row.get("machine_id", ""), result)
        tracker_text.value = "Tracking command..."
        tracker_text.update()

        def on_update(t: CommandTracker):
            def _ui():
                tracker_text.value = f"{t.action}: {t.status} — {t.output or 'waiting for agent...'}"
                tracker_text.update()
                if t._done:
                    self.refresh()
                    self._render_table()
                    self._table_host.update()

            self.page.run_thread(_ui)

        tracker.poll_until_done(on_update)

    def _revoke(self, row, message, dlg, tracker_text):
        result = LicenseAdminService().revoke(
            row.get("license_key") or "",
            row.get("machine_id"),
            message or "License revoked.",
        )
        self._notify(result)
        if result.get("success"):
            self._track("revoke_license", row, result, tracker_text)

    def _restore(self, row, dlg, tracker_text):
        result = LicenseAdminService().restore(
            row.get("license_key") or "",
            row.get("machine_id"),
        )
        self._notify(result)
        if result.get("success"):
            self._track("clear_revoke", row, result, tracker_text)

    def _quick_cmd(self, row, action, params, dlg, tracker_text):
        result = CommandService().queue(row.get("machine_id", ""), action, params)
        self._notify(result)
        if result.get("success"):
            self._track(action, row, result, tracker_text)

    def _notify(self, result: dict):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(result.get("message", ""), color=T.C_TEXT),
            bgcolor=T.C_PANEL,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _export_csv(self, e):
        rows = self._filtered_rows()
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["hostname", "machine_id", "license_key", "biblioq_version", "status", "last_seen_at"])
        for r in rows:
            w.writerow([
                r.get("hostname", ""),
                r.get("machine_id", ""),
                r.get("license_key", ""),
                r.get("biblioq_version", ""),
                r.get("status", ""),
                r.get("last_seen_at", ""),
            ])
        self.page.set_clipboard(buf.getvalue())
        self._notify({"message": f"Copied {len(rows)} rows to clipboard (CSV)."})

    def _close_dlg(self, dlg):
        dlg.open = False
        self.page.update()
