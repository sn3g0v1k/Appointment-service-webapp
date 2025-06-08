import flet as ft
from webapp.database import get_specialists, get_time_on_specialist, get_services_by_specialist
from icecream import ic

from .settings import plogo, pspecialist1


def gen_text(text, size):
    return ft.Text(
        spans=[
            ft.TextSpan(
                text,
                ft.TextStyle(
                    size=size,
                    font_family="Consolas"
                ),
            ),
        ]
    )

def generate_header(page):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_LEFT, on_click=lambda _: page.go("/")),
                ft.GestureDetector(content=header_row(), on_tap=lambda _: page.go("/info"))
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor=ft.Colors.GREY_200,
        border_radius=10,
        padding=10,
    )

def header_row():
    return ft.Row(
        controls=[
            ft.Image(
                src=plogo,
                width=50,
                height=50,
                fit=ft.ImageFit.CONTAIN,
            ),
            ft.Column(
                controls=[
                    gen_text("Выбрать специалиста", 20),
                ],
                spacing=0,
            )
        ],
        alignment=ft.MainAxisAlignment.START,
    )

def button_clicked(name, profession, page):
    data = get_time_on_specialist(name, profession)
    ic(data, "got from database")
    page.session.set("employee_data", data)
    page.session.set("employee_name", name)
    page.go("/choose_time")


def generate_worker_row_column(name, profession, image_src, rewiews, page):
    return ft.Column(controls=[ft.Container(
        content=ft.Column(
            controls=
            generate_worker_row(name, profession, image_src, rewiews),
            spacing=10,
        ),
        padding=10,
    ),
    ft.Container(
        content=ft.ElevatedButton(
            content=gen_text("Выбрать время ", 16),
            bgcolor="#4b8c48",
            color=ft.Colors.BLACK,
            on_click=lambda _: button_clicked(name, profession, page)
        ),
        padding=ft.padding.only(top=20),
    )])

def generate_worker_row(name, profession, image_src, rewiews):
    return [ft.Row(
                            controls=[
                                ft.Image(
                                    src=image_src,
                                    width=50,
                                    height=50,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                ft.Column(
                                    controls=[
                                        gen_text(name, 16),
                                        gen_text(profession, 14),
                                        ft.Row(
                                            controls=[
                                                ft.Icon(name=ft.icons.STAR, color=ft.Colors.YELLOW, size=18),
                                                ft.Icon(name=ft.icons.STAR, color=ft.Colors.YELLOW, size=18),
                                                ft.Icon(name=ft.icons.STAR, color=ft.Colors.YELLOW, size=18),
                                                ft.Icon(name=ft.icons.STAR, color=ft.Colors.YELLOW, size=18),
                                                ft.Icon(name=ft.icons.STAR, color=ft.Colors.YELLOW, size=18),
                                                gen_text(rewiews, 14),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                    ],
                                    spacing=5,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
    ]

#generate_worker_row_column("@sn3g0v1k20 Aurudin", "тренер по гандболу", f"/specialist1.jpg",
#                                       "1 отзывов")

def generate_specialist_column(page):
    controls = [generate_header(page),]
    sps = get_specialists()
    for sp in sps:
        controls.append(generate_worker_row_column(sp[0], get_services_by_specialist(sp[0]), pspecialist1, "5 отзывов", page))
    return ft.Column(
        controls=controls,
        spacing=10,
        scroll=ft.ScrollMode.ADAPTIVE
    )
