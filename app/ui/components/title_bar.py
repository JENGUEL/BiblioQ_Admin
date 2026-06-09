"""Custom title bar — cyberpunk."""

import flet as ft
from app import theme as T


class TitleBar:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.WindowDragArea(
                content=ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    width=12,
                                    height=12,
                                    border_radius=6,
                                    bgcolor="#FF2BD6",
                                    on_click=lambda e: self._close(),
                                ),
                                ft.Container(
                                    width=12,
                                    height=12,
                                    border_radius=6,
                                    bgcolor=T.C_NEON_CYAN,
                                    on_click=lambda e: setattr(
                                        self.page.window, "minimized", True
                                    ),
                                ),
                            ],
                            spacing=6,
                        ),
                        ft.Container(expand=True),
                        ft.Text(
                            "BIBLIOQ // ADMIN",
                            size=11,
                            color=T.C_NEON_CYAN,
                            font_family=T.FONT,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(expand=True),
                        ft.Container(width=40),
                    ],
                ),
            ),
            height=36,
            bgcolor=T.C_PANEL_ALT,
            border=ft.Border.only(bottom=ft.BorderSide(1, T.C_BORDER)),
            padding=ft.Padding.symmetric(horizontal=12),
        )

    def _close(self):
        self.page.window.destroy()
