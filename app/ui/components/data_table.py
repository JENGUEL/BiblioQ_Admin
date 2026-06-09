"""Simple data table wrapper — cyberpunk styling."""

import flet as ft
from app import theme as T


def build_table(columns: list[str], rows: list[list[str]], on_row_click=None) -> ft.Container:
    cols = [
        ft.DataColumn(
            ft.Text(c, weight=ft.FontWeight.BOLD, font_family=T.FONT, color=T.C_NEON_CYAN, size=12)
        )
        for c in columns
    ]
    data_rows = []
    for idx, row in enumerate(rows):
        cells = [
            ft.DataCell(ft.Text(str(cell), font_family=T.FONT, size=12, color=T.C_TEXT))
            for cell in row
        ]
        dr = ft.DataRow(cells=cells)
        if on_row_click:
            dr.on_select_change = lambda e, i=idx: on_row_click(i)
        data_rows.append(dr)

    table = ft.DataTable(
        columns=cols,
        rows=data_rows,
        border=ft.Border.all(1, T.C_BORDER),
        heading_row_color=T.C_PANEL_ALT,
        data_row_color={ft.ControlState.HOVERED: T.C_PANEL_ALT},
    )
    return T.panel_container(
        ft.Column([table], scroll=ft.ScrollMode.AUTO),
        padding=8,
    )


def status_chip(status: str) -> ft.Container:
    color = T.status_color(status)
    return ft.Container(
        content=ft.Text((status or "?").upper(), size=10, color=T.C_BG, font_family=T.FONT, weight=ft.FontWeight.BOLD),
        bgcolor=color,
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
    )
