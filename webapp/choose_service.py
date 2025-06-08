import flet as ft
from icecream import ic

from webapp.database import service_n_cost_on_specialist_n_time
from .settings import plogo, company_name, office_adress


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
                ft.IconButton(icon=ft.Icons.ARROW_LEFT, on_click=lambda _: page.go("/")),
                ft.GestureDetector(content=header_row(), on_tap=lambda _: page.go("/choose_specialist"))
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
                    gen_text("Выбрать услугу", 20),
                ],
                spacing=0,
            )
        ],
        alignment=ft.MainAxisAlignment.START,
    )


# def convert_list_into_dict(list):
#     ic(list)
#     dictionary = {}
#     for cortage in list:
#         dictionary[cortage[0]] = cortage[1]
#     return dictionary

def get_services(page):
    cort = page.session.get("nametimedate")
    ic(cort)
    data = service_n_cost_on_specialist_n_time(cort[0], cort[1], cort[2])
    ic(data)
    # return convert_list_into_dict(data)
    return data

def button_pressed(services):
    ic(services.value)




def generate_service_column(page):
    # Данные услуг
    services = get_services(page)

    def build_services():
        return ft.RadioGroup(ft.Column([
            *[
                ft.Row([
                    ft.Column([
                        ft.Text(service[1]),
                        ft.Text(service[0], size=14)
                    ], expand=True),
                    ft.Radio(width=30, value=service[1])
                ]) for service in services
            ]
        ]))

    servviceess = build_services()
    return ft.Column(
        [
            ft.Container(
                content=ft.Column([
                    generate_header(page),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(company_name, size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(office_adress, size=14)
                            ]),
                            servviceess
                        ]),
                        padding=20
                    )
                ]),
                expand=True
            ),
            ft.Column(
                [
                    ft.ElevatedButton(
                        content=gen_text("Cоздать запись", 16),
                        bgcolor="#4b8c48",
                        color=ft.Colors.BLACK,
                        on_click=lambda _: button_pressed(servviceess)
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
        ]
    )
