"""BiblioQ Admin cyberpunk theme tokens."""

import flet as ft

# Legacy aliases
C_ORANGE = "#00E5FF"
C_ORANGE_DEEP = "#00B8D4"
C_ORANGE_LT = "#12182B"
C_ORANGE_MID = "#1E3A5F"
C_ORANGE_HL = "#0D2137"
C_BG = "#0B0E17"
C_DARK = "#E8F4FF"
C_GREY = "#7A8FA6"
C_WHITE = "#E8F4FF"
C_GREEN = "#39FF14"
C_RED = "#FF2BD6"
C_BLUE = "#00E5FF"

C_PANEL = "#12182B"
C_PANEL_ALT = "#0D1220"
C_NEON_CYAN = "#00E5FF"
C_NEON_MAGENTA = "#FF2BD6"
C_NEON_GREEN = "#39FF14"
C_TEXT = "#E8F4FF"
C_MUTED = "#7A8FA6"
C_BORDER = "#1E3A5F"

FONT = "Poppins"
RADIUS_CARD = 12
RADIUS_BTN = 8


def panel_border() -> ft.Border:
    return ft.Border.all(1, C_NEON_CYAN)


def neon_button_style(bg: str = C_NEON_CYAN) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        bgcolor=bg,
        color=C_BG,
        shape=ft.RoundedRectangleBorder(radius=RADIUS_BTN),
    )


def page_title(text: str) -> ft.Text:
    return ft.Text(
        text,
        size=24,
        weight=ft.FontWeight.BOLD,
        font_family=FONT,
        color=C_TEXT,
    )


def status_color(status: str) -> str:
    s = (status or "").lower()
    if s == "active":
        return C_NEON_GREEN
    if s in ("revoked", "failed"):
        return C_NEON_MAGENTA
    if s in ("offline", "expired"):
        return C_MUTED
    return C_NEON_CYAN


def panel_container(content: ft.Control, **kwargs) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=C_PANEL,
        border=panel_border(),
        border_radius=RADIUS_CARD,
        padding=kwargs.get("padding", 16),
        expand=kwargs.get("expand", False),
    )
