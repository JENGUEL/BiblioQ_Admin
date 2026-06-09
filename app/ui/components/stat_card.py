"""Reusable stat card — cyberpunk."""

import flet as ft
from app import theme as T


class StatCard:
    def __init__(self, title: str, value: str, accent: str = T.C_NEON_CYAN):
        self.title = title
        self.value = value
        self.accent = accent

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(self.title, size=11, color=T.C_MUTED, font_family=T.FONT),
                    ft.Text(
                        self.value,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=self.accent,
                        font_family=T.FONT,
                    ),
                ],
                spacing=4,
            ),
            bgcolor=T.C_PANEL,
            border=ft.Border.all(1, self.accent),
            border_radius=T.RADIUS_CARD,
            padding=ft.Padding.all(16),
            expand=True,
        )
