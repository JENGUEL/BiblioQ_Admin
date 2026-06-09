"""Crash reports page."""

import flet as ft
from app import theme as T
from app.ui.components.data_table import build_table
from app.services.crash_service import CrashService


class ErrorsPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self._table_host = ft.Container()
        self._reports = []

    def build(self) -> ft.Control:
        self.refresh()
        self._render()
        return ft.Column(
            [
                T.page_title("Error reports"),
                ft.Container(height=8),
                self._table_host,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh(self):
        self._reports = CrashService().list_reports(limit=100)

    def _render(self):
        rows = [
            [
                (r.get("occurred_at", "") or "")[:19],
                r.get("machine_id", "")[:12],
                r.get("error_type", ""),
                "Yes" if r.get("resolved") else "No",
                (r.get("stack_trace", "") or "")[:60],
            ]
            for r in self._reports
        ]
        self._table_host.content = build_table(
            ["When", "Machine", "Type", "Resolved", "Trace (preview)"],
            rows or [["No crash reports", "", "", "", ""]],
            on_row_click=self._toggle_resolved,
        )

    def _toggle_resolved(self, index: int):
        if index >= len(self._reports):
            return
        r = self._reports[index]
        new_val = not r.get("resolved", False)
        CrashService().set_resolved(r.get("id"), new_val)
        self.refresh()
        self._render()
        self._table_host.update()
