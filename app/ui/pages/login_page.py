"""Admin login page — cyberpunk."""

import flet as ft
from app import theme as T
from app.services.auth_service import AuthService
from app.auth.session import Session


class LoginPage:
    def __init__(self, page: ft.Page, on_success):
        self.page = page
        self.on_success = on_success
        self._user = ft.TextField(
            label="Username",
            value="admin",
            border_color=T.C_BORDER,
            color=T.C_TEXT,
        )
        self._pass = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            border_color=T.C_BORDER,
            color=T.C_TEXT,
        )
        self._msg = ft.Text("", size=12, color=T.C_NEON_MAGENTA, font_family=T.FONT)

    def build(self) -> ft.Control:
        return ft.Container(
            bgcolor=T.C_BG,
            expand=True,
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "BIBLIOQ",
                                    size=40,
                                    weight=ft.FontWeight.BOLD,
                                    color=T.C_NEON_CYAN,
                                    font_family=T.FONT,
                                ),
                                ft.Text(
                                    "Remote installation control",
                                    size=14,
                                    color=T.C_MUTED,
                                    font_family=T.FONT,
                                ),
                                ft.Container(height=24),
                                ft.Text(
                                    "Manage licenses, agents, and telemetry across your school network.",
                                    size=12,
                                    color=T.C_MUTED,
                                    font_family=T.FONT,
                                    width=320,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        expand=True,
                        padding=48,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Sign in",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    font_family=T.FONT,
                                    color=T.C_TEXT,
                                ),
                                ft.Container(height=8),
                                self._user,
                                self._pass,
                                self._msg,
                                ft.ElevatedButton(
                                    content=ft.Text("Login", font_family=T.FONT, weight=ft.FontWeight.BOLD),
                                    style=T.neon_button_style(),
                                    height=44,
                                    on_click=self._submit,
                                ),
                            ],
                            spacing=12,
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        ),
                        width=360,
                        bgcolor=T.C_PANEL,
                        border=ft.Border.all(1, T.C_NEON_CYAN),
                        border_radius=16,
                        padding=32,
                        margin=ft.Margin.only(right=48),
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    def _submit(self, e):
        result = AuthService().login(self._user.value or "", self._pass.value or "")
        if result.get("success"):
            Session.login(result.get("user") or {"username": self._user.value or "admin"})
            self.on_success()
        else:
            self._msg.value = result.get("message", "Login failed.")
            self._msg.update()
