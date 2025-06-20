import flet as ft
from icecream import ic

from webapp.database import service_n_cost_on_specialist_n_time, make_booking
from .settings import plogo, company_name, office_adress


def gen_text(text, size, weight=ft.FontWeight.NORMAL, color=ft.colors.BLACK):
    return ft.Text(
        text,
        size=size,
        weight=weight,
        color=color,
        font_family="Roboto"
    )


def generate_header(page):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=ft.colors.BLUE,
                    tooltip="Назад",
                    on_click=lambda _: page.go("/")
                ),
                ft.GestureDetector(
                    content=header_row(),
                    on_tap=lambda _: page.go("/choose_specialist")
                )
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor=ft.colors.SURFACE_VARIANT,
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
                    gen_text("Выбрать услугу", 24, ft.FontWeight.BOLD),
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

def button_pressed(page, services):
    if services.value is None:
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Пожалуйста, выберите услугу"),
                bgcolor=ft.colors.RED_400,
            )
        )
        return
    
    try:
        service = services.value
        cort = page.session.get("nametimedate")
        user_id = page.session.get("user_id")
        ic(service, "          ", cort, user_id)
        make_booking(user_id, service, cort[0], cort[2], cort[1])
        
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("✅ Запись успешно создана!"),
                bgcolor=ft.colors.GREEN_400,
            )
        )
        page.go("/profile")
    except Exception as e:
        ic(e)
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("❌ Ошибка при создании записи"),
                bgcolor=ft.colors.RED_400,
            )
        )





def generate_service_column(page):
    services = get_services(page)

    def build_services():
        return ft.RadioGroup(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            gen_text(service[1], 18, ft.FontWeight.BOLD),
                            gen_text(f"Стоимость: {service[0]} ₽", 16, color=ft.colors.BLUE_700)
                        ], expand=True),
                        ft.Radio(width=30, value=service[1])
                    ]),
                    padding=10,
                    border_radius=8,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    margin=ft.margin.only(bottom=10)
                ) for service in services
            ])
        )

    servviceess = build_services()
    
    return ft.Column(
        [
            ft.Container(
                content=ft.Column([
                    generate_header(page),
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Column([
                                    gen_text(company_name, 24, ft.FontWeight.BOLD),
                                    gen_text(office_adress, 16, color=ft.colors.GREY_700)
                                ]),
                                padding=20,
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                border_radius=10,
                                margin=ft.margin.only(bottom=20)
                            ),
                            gen_text("Доступные услуги:", 20, ft.FontWeight.BOLD),
                            servviceess
                        ]),
                        padding=20
                    )
                ]),
                expand=True
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    text="Создать запись",
                    icon=ft.icons.CALENDAR_MONTH,
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLUE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    on_click=lambda _: button_pressed(page, servviceess)
                ),
                padding=20,
                alignment=ft.alignment.center_right
            )
        ]
    )
