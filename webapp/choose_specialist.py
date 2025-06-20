import flet as ft
from webapp.database import get_specialists, get_time_on_specialist, get_services_by_specialist
from icecream import ic

from .settings import plogo, pspecialist1


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
                    on_tap=lambda _: page.go("/info")
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
                    gen_text("Выбрать специалиста", 24, ft.FontWeight.BOLD),
                ],
                spacing=0,
            )
        ],
        alignment=ft.MainAxisAlignment.START,
    )

def button_clicked(name, profession, page):
    try:
        full_name = f"{name} {profession}"
        page.session.set("employee_name", full_name)
        data = get_time_on_specialist(name, profession)
        ic(data, "got from database")
        page.session.set("employee_data", data)
        # page.session.set("employee_name", name)
        page.go("/choose_time")
    except Exception as e:
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("❌ Ошибка при выборе специалиста"),
                bgcolor=ft.colors.RED_400,
            )
        )
def generate_specialist_card(name, profession, image_src, reviews, page):
    full_name = f"{name} {profession}"
    ic()
    services = get_services_by_specialist(full_name)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src=image_src,
                                width=100,
                                height=100,
                                fit=ft.ImageFit.COVER,
                            ),
                            width=100,
                            height=100,
                            border_radius=50,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        ),
                        ft.Column(
                            controls=[
                                gen_text(name, 20, ft.FontWeight.BOLD),
                                gen_text(profession, 16, color=ft.colors.GREY_700),
                                ft.Container(
                                    content=ft.Column([
                                        gen_text("Услуги:", 16, ft.FontWeight.BOLD),
                                        *[gen_text(f"• {service}", 14, color=ft.colors.GREY_700) for service in services]
                                    ],
                                    spacing=5
                                    ),
                                    padding=10,
                                    bgcolor=ft.colors.SURFACE_VARIANT,
                                    border_radius=8,
                                ),
                                ft.Row(
                                    controls=[
                                        *[ft.Icon(name=ft.icons.STAR, color=ft.colors.AMBER, size=20) for _ in range(5)],
                                        gen_text(f"{reviews}", 14, color=ft.colors.GREY_700),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                            ],
                            spacing=10,
                            expand=True,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Выбрать время",
                        icon=ft.icons.CALENDAR_MONTH,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=lambda _: button_clicked(name, profession, page)
                    ),
                    padding=ft.padding.only(top=20),
                    alignment=ft.alignment.center_right,
                )
            ],
            spacing=10,
        ),
        padding=20,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=10,
        margin=ft.margin.only(bottom=20),
    )

# def generate_specialist_card(name, profession, image_src, reviews, page):
#     # services = get_services_by_specialist(name)
#     services = get_services_by_specialist(f"{name} {profession}")
#     return ft.Container(
#         content=ft.Column(
#             controls=[
#                 ft.Row(
#                     controls=[
#                         ft.Container(
#                             content=ft.Image(
#                                 src=image_src,
#                                 width=100,
#                                 height=100,
#                                 fit=ft.ImageFit.COVER,
#                             ),
#                             width=100,
#                             height=100,
#                             border_radius=50,
#                             clip_behavior=ft.ClipBehavior.HARD_EDGE,
#                         ),
#                         ft.Column(
#                             controls=[
#                                 gen_text(name, 20, ft.FontWeight.BOLD),
#                                 gen_text(profession, 16, color=ft.colors.GREY_700),
#                                 ft.Container(
#                                     content=ft.Column(
#                                     #     [
#                                     #     gen_text("Услуги:", 16, ft.FontWeight.BOLD),
#                                     #     *[gen_text(f"• {service}", 14, color=ft.colors.GREY_700) for service in services]
#                                     # ],
#                                         controls=[
#                                             gen_text("Услуги:", 16, ft.FontWeight.BOLD),
#                                             *(
#                                                 [gen_text(f"• {service}", 14, color=ft.colors.GREY_700) for service in
#                                                  services]
#                                                 if services else
#                                                 [gen_text("Нет доступных услуг", 14, color=ft.colors.RED)]
#                                             )
#                                         ],
#                                     spacing=5
#                                     ),
#                                     padding=10,
#                                     bgcolor=ft.colors.SURFACE_VARIANT,
#                                     border_radius=8,
#                                 ),
#                                 ft.Row(
#                                     controls=[
#                                         *[ft.Icon(name=ft.icons.STAR, color=ft.colors.AMBER, size=20) for _ in range(5)],
#                                         gen_text(f"{reviews}", 14, color=ft.colors.GREY_700),
#                                     ],
#                                     alignment=ft.MainAxisAlignment.START,
#                                 ),
#                             ],
#                             spacing=10,
#                             expand=True,
#                         ),
#                     ],
#                     vertical_alignment=ft.CrossAxisAlignment.START,
#                 ),
#                 ft.Container(
#                     content=ft.ElevatedButton(
#                         text="Выбрать время",
#                         icon=ft.icons.CALENDAR_MONTH,
#                         style=ft.ButtonStyle(
#                             color=ft.colors.WHITE,
#                             bgcolor=ft.colors.BLUE,
#                             shape=ft.RoundedRectangleBorder(radius=10),
#                         ),
#                         on_click=lambda _: button_clicked(name, profession, page)
#                     ),
#                     padding=ft.padding.only(top=20),
#                     alignment=ft.alignment.center_right,
#                 )
#             ],
#             spacing=10,
#         ),
#         padding=20,
#         bgcolor=ft.colors.SURFACE_VARIANT,
#         border_radius=10,
#         margin=ft.margin.only(bottom=20),
#     )

def generate_specialist_column(page):
    try:
        specialists = get_specialists()
        return ft.Column(
            controls=[
                generate_header(page),
                ft.Container(
                    content=ft.Column([
                        gen_text("Наши специалисты:", 24, ft.FontWeight.BOLD),
                        *[generate_specialist_card(sp[0], sp[1], pspecialist1, "5 отзывов", page) for sp in specialists]
                    ],
                    spacing=20
                    ),
                    padding=20
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.ADAPTIVE
        )
    except Exception as e:
        ic(e)
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("❌ Ошибка при загрузке списка специалистов"),
                bgcolor=ft.colors.RED_400,
            )
        )
        return ft.Column(
            controls=[
                generate_header(page),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.ERROR_OUTLINE, size=50, color=ft.colors.RED),
                        gen_text("Не удалось загрузить список специалистов", 20, color=ft.colors.RED)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                    ),
                    padding=20
                )
            ]
        )
