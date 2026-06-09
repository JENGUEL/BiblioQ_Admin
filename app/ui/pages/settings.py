"""Settings page."""

import flet as ft
from app import theme as T
from app.config import load_config, save_config
from app.utils.crypto import encrypt_config_value, decrypt_config_value
from app.utils.supabase_url import normalize_supabase_url
from app.services.supabase_client import SupabaseClient
from app.services.auth_service import AuthService
from app.auth.session import Session


class SettingsPage:
    def __init__(self, page: ft.Page, realtime=None):
        self.page = page
        self.realtime = realtime
        cfg = load_config()
        self._url = ft.TextField(
            label="Supabase URL",
            value=cfg.get("supabase_url", ""),
            hint_text="https://YOUR_PROJECT.supabase.co",
            border_color=T.C_BORDER,
            color=T.C_TEXT,
        )
        self._service = ft.TextField(
            label="Service role key",
            password=True,
            can_reveal_password=True,
            value=decrypt_config_value(cfg.get("supabase_service_key", "")),
            border_color=T.C_BORDER,
            color=T.C_TEXT,
        )
        self._admin_token = ft.TextField(
            label="Admin API token (edge functions)",
            password=True,
            can_reveal_password=True,
            value=decrypt_config_value(cfg.get("admin_api_token", "")),
            border_color=T.C_BORDER,
            color=T.C_TEXT,
        )
        self._agent_key = ft.TextField(
            label="Agent API key",
            password=True,
            can_reveal_password=True,
            value=decrypt_config_value(cfg.get("agent_api_key", "")),
            border_color=T.C_BORDER,
            color=T.C_TEXT,
        )
        self._old_pass = ft.TextField(label="Current password", password=True, border_color=T.C_BORDER)
        self._new_pass = ft.TextField(label="New password", password=True, border_color=T.C_BORDER)
        self._status = ft.Text("", color=T.C_MUTED, font_family=T.FONT)
        self._health = ft.Text("Connection health: not checked", size=12, color=T.C_MUTED, font_family=T.FONT)

    def build(self) -> ft.Control:
        self._refresh_health()
        return ft.Column(
            [
                T.page_title("Settings"),
                ft.Container(height=8),
                T.panel_container(
                    ft.Column(
                        [
                            ft.Text("Connection health", size=14, weight=ft.FontWeight.W_500, color=T.C_NEON_CYAN),
                            self._health,
                            ft.ElevatedButton(
                                "Run health check",
                                style=T.neon_button_style(T.C_PANEL_ALT),
                                on_click=self._health_check,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=16,
                ),
                ft.Container(height=12),
                ft.Text("Supabase connection", size=14, weight=ft.FontWeight.W_500, color=T.C_TEXT),
                self._url,
                ft.Text(
                    "Use the project URL only (no /rest/v1/).",
                    size=11,
                    color=T.C_MUTED,
                    font_family=T.FONT,
                ),
                self._service,
                self._admin_token,
                self._agent_key,
                ft.Row(
                    [
                        ft.ElevatedButton("Save", style=T.neon_button_style(), on_click=self._save),
                        ft.OutlinedButton("Test connection", on_click=self._test),
                        ft.OutlinedButton(
                            "Create agent config on this PC",
                            on_click=self._create_agent_config,
                        ),
                    ],
                    wrap=True,
                ),
                self._status,
                ft.Divider(color=T.C_BORDER),
                ft.Text("Change admin password", size=14, weight=ft.FontWeight.W_500, color=T.C_TEXT),
                self._old_pass,
                self._new_pass,
                ft.ElevatedButton(
                    "Update password",
                    style=T.neon_button_style(T.C_NEON_MAGENTA),
                    on_click=self._change_pass,
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def _refresh_health(self):
        if self.realtime and self.realtime.connected:
            self._health.value = "Connection health: Supabase OK · Realtime polling active"
            self._health.color = T.C_NEON_GREEN
        elif SupabaseClient().configured:
            self._health.value = "Connection health: configured (realtime idle)"
            self._health.color = T.C_MUTED
        else:
            self._health.value = "Connection health: not configured"
            self._health.color = T.C_NEON_MAGENTA

    def _health_check(self, e):
        db = SupabaseClient()
        ok, msg = db.test_connection()
        rt_ok, rt_msg = (False, "N/A")
        if self.realtime:
            rt_ok, rt_msg = self.realtime.ping()
        agent_ok = bool((self._agent_key.value or "").strip())
        lines = [
            f"Supabase REST: {'OK' if ok else 'FAIL'} — {msg}",
            f"Realtime: {'OK' if rt_ok else 'FAIL'} — {rt_msg}",
            f"Agent API key: {'set' if agent_ok else 'missing'}",
        ]
        self._health.value = "\n".join(lines)
        self._health.color = T.C_NEON_GREEN if ok else T.C_NEON_MAGENTA
        self._health.update()

    def _field_values(self) -> dict:
        try:
            url = normalize_supabase_url(self._url.value or "")
        except ValueError as ex:
            raise ValueError(str(ex)) from ex
        return {
            "supabase_url": url,
            "supabase_service_key": encrypt_config_value(self._service.value or ""),
            "admin_api_token": encrypt_config_value(self._admin_token.value or ""),
            "agent_api_key": encrypt_config_value(self._agent_key.value or ""),
        }

    def _save(self, e, silent: bool = False):
        try:
            data = self._field_values()
        except ValueError as ex:
            self._status.value = str(ex)
            self._status.color = T.C_NEON_MAGENTA
            self._status.update()
            return False
        save_config(data)
        self._url.value = data["supabase_url"]
        if not silent:
            self._status.value = "Settings saved."
            self._status.color = T.C_MUTED
            self._status.update()
        self._url.update()
        self._refresh_health()
        return True

    def _test(self, e):
        try:
            url = normalize_supabase_url(self._url.value or "")
        except ValueError as ex:
            self._status.value = str(ex)
            self._status.color = T.C_NEON_MAGENTA
            self._status.update()
            return

        service_key = (self._service.value or "").strip()
        if not service_key:
            self._status.value = "Service role key is required."
            self._status.color = T.C_NEON_MAGENTA
            self._status.update()
            return

        ok, msg = SupabaseClient(base_url=url, service_key=service_key).test_connection()
        if ok:
            self._url.value = url
            self._save(e, silent=True)
            msg = "Connected to Supabase. Settings saved."
        self._status.value = msg
        self._status.color = T.C_NEON_GREEN if ok else T.C_NEON_MAGENTA
        self._status.update()

    def _create_agent_config(self, e):
        from app.services.agent_setup import write_agent_config

        try:
            url = normalize_supabase_url(self._url.value or "")
            agent_key = (self._agent_key.value or "").strip()
            if not agent_key:
                raise ValueError("Agent API key is required.")
            path = write_agent_config(url, agent_key)
            self._status.value = f"Agent config written: {path}"
            self._status.color = T.C_NEON_GREEN
        except Exception as ex:
            self._status.value = str(ex)[:120]
            self._status.color = T.C_NEON_MAGENTA
        self._status.update()

    def _change_pass(self, e):
        result = AuthService().change_password(
            Session.username(),
            self._old_pass.value or "",
            self._new_pass.value or "",
        )
        self._status.value = result.get("message", "")
        self._status.color = T.C_NEON_GREEN if result.get("success") else T.C_NEON_MAGENTA
        self._status.update()
