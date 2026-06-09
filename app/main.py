"""Flet application entry."""

import flet as ft
from app import __app_name__, __version__
from app.auth.session import Session
from app.ui.pages.login_page import LoginPage
from app.ui.app_shell import AppShell
from app.utils.logger import logger


def main(page: ft.Page):
    logger.info("Starting %s v%s", __app_name__, __version__)
    page.title = f"{__app_name__} v{__version__}"
    page.window.width = 1200
    page.window.height = 800
    page.window.frameless = True
    page.window.title_bar_hidden = True
    page.padding = 0
    page.bgcolor = "#FFF3E2"
    page.theme_mode = ft.ThemeMode.LIGHT

    def show_dashboard():
        page.controls.clear()
        shell = AppShell(page)
        page.add(shell.build())
        page.update()

    if Session.is_logged_in():
        show_dashboard()
        return

    login = LoginPage(page, show_dashboard)
    page.add(login.build())
