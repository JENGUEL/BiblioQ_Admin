"""Admin sidebar navigation — cyberpunk labeled nav."""

import flet as ft
from app import theme as T

NAV_ITEMS = [
    ("Dashboard", ft.Icons.DASHBOARD),
    ("Installations", ft.Icons.COMPUTER),
    ("Licenses", ft.Icons.VPN_KEY),
    ("Commands", ft.Icons.TERMINAL),
    ("Errors", ft.Icons.ERROR_OUTLINE),
    ("Audit", ft.Icons.HISTORY),
    ("Settings", ft.Icons.SETTINGS),
]


class Sidebar:
    def __init__(self, page: ft.Page, on_navigate, on_logout):
        self.page = page
        self.on_navigate = on_navigate
        self.on_logout = on_logout
        self._selected = 0
        self._buttons: list[ft.Container] = []

    def build(self) -> ft.Container:
        self._buttons = []
        nav_controls = []
        for i, (label, icon) in enumerate(NAV_ITEMS):
            row = self._nav_item(i, label, icon)
            self._buttons.append(row)
            nav_controls.append(row)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=12),
                    ft.Text(
                        "BIBLIOQ",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=T.C_NEON_CYAN,
                        font_family=T.FONT,
                    ),
                    ft.Text("Remote Admin", size=10, color=T.C_MUTED, font_family=T.FONT),
                    ft.Container(height=16),
                    *nav_controls,
                    ft.Container(expand=True),
                    ft.TextButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.LOGOUT, size=16, color=T.C_NEON_MAGENTA),
                                ft.Text("Logout", size=12, color=T.C_NEON_MAGENTA, font_family=T.FONT),
                            ],
                            spacing=8,
                        ),
                        on_click=lambda e: self.on_logout(),
                    ),
                    ft.Container(height=8),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            width=180,
            bgcolor=T.C_PANEL,
            border=ft.Border.all(1, T.C_BORDER),
            border_radius=12,
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            margin=ft.Margin.only(left=8, top=8, bottom=8),
        )

    def _nav_item(self, index: int, label: str, icon) -> ft.Container:
        selected = index == self._selected
        color = T.C_NEON_CYAN if selected else T.C_MUTED
        bg = T.C_PANEL_ALT if selected else "transparent"

        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=18, color=color),
                    ft.Text(label, size=12, color=color, font_family=T.FONT),
                ],
                spacing=10,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=10),
            border_radius=8,
            bgcolor=bg,
            border=ft.Border.all(1, T.C_NEON_CYAN) if selected else None,
            on_click=lambda e, idx=index: self._click(idx),
            ink=True,
        )

    def _click(self, index: int):
        self._selected = index
        self.on_navigate(index)

    def set_selected(self, index: int):
        self._selected = index
        for i, btn in enumerate(self._buttons):
            selected = i == index
            color = T.C_NEON_CYAN if selected else T.C_MUTED
            btn.bgcolor = T.C_PANEL_ALT if selected else "transparent"
            btn.border = ft.Border.all(1, T.C_NEON_CYAN) if selected else None
            if btn.content and isinstance(btn.content, ft.Row):
                for c in btn.content.controls:
                    if isinstance(c, ft.Icon):
                        c.color = color
                    elif isinstance(c, ft.Text):
                        c.color = color
