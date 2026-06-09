"""Remote commands page."""

import flet as ft
from app import theme as T
from app.ui.components.data_table import build_table
from app.services.command_service import CommandService, ALLOWED_ACTIONS
from app.services.installation_service import InstallationService


class CommandsPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self._machine = ft.Dropdown(label="Target machine", width=400)
        self._action = ft.Dropdown(
            label="Action",
            width=400,
            options=[ft.dropdown.Option(a) for a in ALLOWED_ACTIONS],
        )
        self._params = ft.TextField(label="Params JSON", value="{}", multiline=True, min_lines=2)
        self._history = ft.Container()

    def build(self) -> ft.Control:
        self._load_machines()
        self.refresh()
        return ft.Column(
            [
                T.page_title("Commands"),
                ft.Container(height=8),
                self._machine,
                self._action,
                self._params,
                ft.ElevatedButton(
                    "Queue command",
                    style=T.neon_button_style(),
                    on_click=self._queue,
                ),
                ft.Container(height=16),
                ft.Text("Recent commands", size=14, font_family=T.FONT, color=T.C_MUTED),
                self._history,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def _load_machines(self):
        rows = InstallationService().list_all(limit=100)
        self._machine.options = [
            ft.dropdown.Option(key=r.get("machine_id"), text=r.get("hostname") or r.get("machine_id"))
            for r in rows
        ] or [ft.dropdown.Option(key="", text="No machines")]

    def _queue(self, e):
        import json
        svc = CommandService()
        try:
            params = json.loads(self._params.value or "{}")
        except json.JSONDecodeError:
            self.page.snack_bar = ft.SnackBar(ft.Text("Invalid JSON in params."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        result = svc.queue(
            self._machine.value or "",
            self._action.value or "show_message",
            params,
        )
        self.page.snack_bar = ft.SnackBar(ft.Text(result.get("message", "")))
        self.page.snack_bar.open = True
        self.refresh()
        self.page.update()

    def refresh(self):
        cmds = CommandService().list_commands(limit=50)
        rows = [
            [
                (c.get("created_at", "") or "")[:19],
                c.get("machine_id", "")[:12],
                c.get("action", ""),
                c.get("status", ""),
            ]
            for c in cmds
        ]
        self._history.content = build_table(
            ["Created", "Machine", "Action", "Status"],
            rows or [["No commands yet", "", "", ""]],
        )
