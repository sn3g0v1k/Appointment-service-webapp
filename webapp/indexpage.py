import flet as ft
from .settings import plogo

def gen_text(text, size):
    return ft.Text(
        spans=[
            ft.TextSpan(
                text,
                ft.TextStyle(
                    size=size,
                    font_family="Caveat",
                    color=ft.Colors.BLACK,
                ),
            ),
        ],
        font_family="Caveat"
    )

def header_row(page):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(
                    src=plogo,
                    width=100,
                    height=100,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Column(
                    controls=[
                        gen_text("Company name", 30),
                        ft.Text("ул. Чернышевского 3", size=12, color=ft.Colors.GREY)
                    ],
                    spacing=0
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.only(left=20, top=20, right=20, bottom=20),
        border_radius=ft.border_radius.all(10),
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 3),
        ),
        on_click=lambda _: page.go("/info")
    )

def generate_row(icon, text, link, page):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(name=icon, color=ft.Colors.GREY, size=24),
                ft.Text(text, size=15, color=ft.Colors.BLACK),
                ft.Container(
                    content=ft.Icon(name=ft.Icons.ARROW_RIGHT, color=ft.Colors.GREY),
                    alignment=ft.alignment.center_right,
                    expand=True
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        border_radius=ft.border_radius.all(10),
        bgcolor=ft.Colors.WHITE,
        margin=ft.margin.only(top=10),
        on_click=lambda _: page.go(link)
    )

def generate_index_column(page: ft.Page):
    return ft.Column(
        controls=[
            header_row(page),
            generate_row(ft.Icons.PEOPLE, "Выбрать тренера", "/choose_specialist", page),
            generate_row(ft.Icons.TIMER_ROUNDED, "Выбрать время", "/date", page),
            generate_row(ft.Icons.SPORTS_VOLLEYBALL_OUTLINED, "Выбрать услугу", "/train", page)
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

# def main(page: ft.Page):
#     page.title = "Training App"
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.vertical_alignment = ft.MainAxisAlignment.START
#     page.add(generate_index_column(page))
#
# ft.app(target=main)