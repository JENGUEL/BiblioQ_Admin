"""Admin app shell."""

import flet as ft
from app import theme as T
from app.ui.sidebar import Sidebar
from app.ui.components.title_bar import TitleBar
from app.ui.pages.dashboard import DashboardPage
from app.ui.pages.installations import InstallationsPage
from app.ui.pages.licenses import LicensesPage
from app.ui.pages.errors import ErrorsPage
from app.ui.pages.commands import CommandsPage
from app.ui.pages.audit import AuditPage
from app.ui.pages.settings import SettingsPage
from app.services.realtime_service import RealtimeService


class AppShell:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.app_shell = self
        self.realtime = RealtimeService()
        self.realtime.start()

        self.pages = [
            DashboardPage(page, self.realtime),
            InstallationsPage(page),
            LicensesPage(page),
            CommandsPage(page),
            ErrorsPage(page),
            AuditPage(page),
            SettingsPage(page, self.realtime),
        ]
        self._views = {}
        self._current = 0
        self._views[0] = self.pages[0].build()

        self.content_area = ft.AnimatedSwitcher(
            content=self._views[0],
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=200,
            expand=True,
        )

        self.title_bar = TitleBar(page)
        self.sidebar = Sidebar(page, self._on_navigate, self._on_logout)

        self.realtime.subscribe(self._on_realtime_event)

    def _on_realtime_event(self, event_type: str, payload: dict):
        if self._current == 0 and hasattr(self.pages[0], "on_realtime"):
            self.pages[0].on_realtime(event_type, payload)
        if self._current == 1 and event_type in ("command", "command_result", "installation"):
            page_obj = self.pages[1]
            if hasattr(page_obj, "_refresh_ui"):
                try:
                    self.page.run_thread(page_obj._refresh_ui)
                except Exception:
                    pass

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor=T.C_BG,
            expand=True,
            content=ft.Column(
                [
                    self.title_bar.build(),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.sidebar.build(),
                                ft.Container(
                                    content=self.content_area,
                                    expand=True,
                                    padding=16,
                                ),
                            ],
                            expand=True,
                        ),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        )

    def _on_navigate(self, index: int):
        if index not in self._views:
            self._views[index] = self.pages[index].build()
        else:
            page_obj = self.pages[index]
            if hasattr(page_obj, "refresh"):
                page_obj.refresh()
            if index == 0 and hasattr(page_obj, "_stats_row"):
                page_obj.refresh()
            if index == 1 and hasattr(page_obj, "_render_table"):
                page_obj._render_table()
            if index == 2 and hasattr(page_obj, "_render"):
                page_obj._render()
            if index == 4 and hasattr(page_obj, "_render"):
                page_obj._render()
            if index == 5 and hasattr(page_obj, "refresh"):
                page_obj.refresh()
            if index == 3 and hasattr(page_obj, "refresh"):
                page_obj.refresh()
        self._current = index
        self.sidebar.set_selected(index)
        self.content_area.content = self._views[index]
        self.content_area.update()

    def _on_logout(self):
        from app.auth.session import Session

        self.realtime.stop()
        Session.logout()
        self.page.controls.clear()
        from app.ui.pages.login_page import LoginPage

        def on_ok():
            self.page.controls.clear()
            shell = AppShell(self.page)
            self.page.add(shell.build())
            self.page.update()

        login = LoginPage(self.page, on_ok)
        self.page.add(login.build())
        self.page.update()
