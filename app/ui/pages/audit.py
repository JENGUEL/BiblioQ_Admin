"""Audit log page."""

import flet as ft
from app import theme as T
from app.ui.components.data_table import build_table
from app.services.audit_service import AuditService


class AuditPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self._table_host = ft.Container()

    def build(self) -> ft.Control:
        self.refresh()
        return ft.Column(
            [
                ft.Row(
                    [
                        T.page_title("Audit Log"),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Refresh",
                            style=T.neon_button_style(),
                            on_click=lambda e: self._refresh_ui(),
                        ),
                    ],
                ),
                ft.Container(height=12),
                self._table_host,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh(self):
        rows = AuditService().list_recent(limit=150)
        table_rows = [
            [
                (r.get("created_at") or "")[:19],
                r.get("actor", ""),
                r.get("action", ""),
                r.get("target_type", ""),
                (r.get("target_id") or "")[:24],
            ]
            for r in rows
        ]
        self._table_host.content = build_table(
            ["When", "Actor", "Action", "Type", "Target"],
            table_rows or [["No audit entries yet", "", "", "", ""]],
        )

    def _refresh_ui(self):
        self.refresh()
        self._table_host.update()
