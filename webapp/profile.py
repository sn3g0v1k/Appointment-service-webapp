from datetime import datetime

import flet as ft
from icecream import ic

from .database import get_bookings_from_user_id, get_profile_pic_and_name


def gen_text(text, size, weight="normal"):
    return ft.Text(
        spans=[
            ft.TextSpan(
                text,
                ft.TextStyle(
                    size=size,
                    font_family="Caveat",
                    color=ft.colors.BLACK,
                    weight=weight
                ),
            ),
        ],
        font_family="Caveat"
    )


def create_schedule_column(page: ft.Page):
    user_id = page.session.get("user_id")
    if user_id is None:
        return ft.Column(
            controls=[
                ft.Text("Вы еще никуда не записаны", size=14, color=ft.Colors.GREY),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )
    bookings = get_bookings_from_user_id(user_id)
    return ft.Column(
        controls=[
            ft.Text(f"{i[0]}    {i[1]}    {i[2]}    {i[3]}", size=14, color=ft.Colors.GREY) for i in bookings
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
    )


def generate_profile_column(page: ft.Page):
    user_id = page.session.get("user_id")
    ic(get_profile_pic_and_name(user_id))
    data = get_profile_pic_and_name(user_id)
    url = get_profile_pic_and_name(user_id)[0]
    us_name = get_profile_pic_and_name(user_id)[1]
    ic(url, us_name)
    return ft.Column(
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ft.CircleAvatar(
                            foreground_image_src=url,
                            # width=160,
                            # height=160,
                            # fit=ft.ImageFit.COVER,
                        ),
                    ft.Column(
                        spacing=5,
                        controls=[
                            gen_text(us_name, 28, "bold"),
                            ft.Text(f"id: {page.session.get('user_id')}", style=ft.TextThemeStyle.BODY_MEDIUM)
                        ]
                    )
                ],
                spacing=15
            ),

            # Информационная область
            ft.Container(
                padding=ft.padding.all(15),
                border_radius=10,
                margin=ft.margin.all(15),
                content=ft.Text(
                    "Это ваш личный профиль. Регистрация была выполнена автоматически с помощью вашего Telegram-аккаунта. Здесь вы можете просматривать информацию о себe и своих записях к нашим специалистам.",
                    style=ft.TextThemeStyle.BODY_MEDIUM,
                    max_lines=6,
                    overflow=ft.TextOverflow.ELLIPSIS
                )
            ),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=create_schedule_column(page),
                            padding=ft.padding.all(10),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            width=page.width,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2,
                ),

                # bgcolor=ft.Colors.WHITE,

                # border=ft.border.all(1, ft.Colors.BLACK),

                border_radius=15,

            )
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.HIDDEN,
    )

# def main(page: ft.Page):
#     page.title = "Профиль"
#     page.theme = ft.Theme(font_family="Caveat")
#     page.add(generate_profile_column(page))
#
# ft.app(target=main)
