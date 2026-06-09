"""Licenses overview page."""

import flet as ft
from app import theme as T
from app.ui.components.data_table import build_table
from app.services.license_service import LicenseAdminService


class LicensesPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self._table_host = ft.Container()
        self._search = ft.TextField(
            label="Search key or school",
            border_color=T.C_BORDER,
            color=T.C_TEXT,
            on_change=lambda e: self._render(),
        )
        self._rows: list = []

    def build(self) -> ft.Control:
        self.refresh()
        self._render()
        return ft.Column(
            [
                ft.Row(
                    [
                        T.page_title("Licenses"),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Refresh",
                            style=T.neon_button_style(),
                            on_click=lambda e: self._refresh_ui(),
                        ),
                    ],
                ),
                ft.Container(height=8),
                self._search,
                ft.Container(height=8),
                self._table_host,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh(self):
        self._rows = LicenseAdminService().list_licenses()

    def _refresh_ui(self):
        self.refresh()
        self._render()
        self._table_host.update()

    def _render(self):
        q = (self._search.value or "").strip().lower()
        rows = self._rows
        if q:
            rows = [
                r
                for r in rows
                if q in (r.get("key") or "").lower() or q in (r.get("school") or "").lower()
            ]
        table_rows = [
            [
                r.get("key", ""),
                r.get("school", "") or "—",
                (r.get("status") or "").upper(),
                (r.get("machine_id") or "")[:16] or "—",
                (r.get("revoked_at") or "")[:19] or "—",
            ]
            for r in rows
        ]
        self._table_host.content = build_table(
            ["Key", "School", "Status", "Machine", "Revoked at"],
            table_rows or [["No licenses", "", "", "", ""]],
        )
