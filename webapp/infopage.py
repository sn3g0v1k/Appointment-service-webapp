from .settings import pmap, plogo
import flet as ft
import webbrowser

def gen_text(text, size):
    return ft.Text(
        spans=[
            ft.TextSpan(
                text,
                ft.TextStyle(
                    size=size,
                    font_family="Caveat",
                ),
            ),
        ],
        font_family="Caveat"
    )

def generate_header(page):
    return ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.ARROW_LEFT, on_click=lambda _: page.go("/"))
        ]
    )

def header_row():
    return ft.Row(
                controls=[
                    ft.Image(
                        src=plogo,
                        width=100,
                        height=100,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    gen_text("Тренировки", 30)
                ]
            )

def generate_row_text(icon, text, size):
    return ft.Row(
        controls=[
            ft.Icon(icon),
            gen_text(text, size)
        ]
    )

def generate_info_column(page):
    return ft.Column(
        controls=[
            generate_header(page),
            header_row(),
            generate_row_text(ft.Icons.PLACE, "ул. Чернышевского 3", 15),
            gen_text("Контакты", 20),
            generate_row_text(ft.Icons.CONTACTS, "+7 917 366 62 91", 15),
            ft.GestureDetector(generate_row_text(ft.Icons.WEB, "www.youtube.ru", 15), on_tap=lambda _: webbrowser.open("https://discord.com")),
            gen_text("Расположение", 20),
            ft.Image(src=pmap)
        ],
    )