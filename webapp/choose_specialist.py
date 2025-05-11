import flet as ft

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
        bgcolor=ft.colors.GREY_200,
        border_radius=10,
        padding=10,
    )

def header_row():
    return ft.Row(
        controls=[
            ft.Image(
                src=f"/personal_photo.jpg",
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


def generate_worker_row_column(name, profession, image_src, rewiews):
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
            content=gen_text("Выбрать услугу", 16),
            bgcolor=ft.colors.YELLOW,
            color=ft.colors.BLACK,
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
                                                ft.Icon(name=ft.icons.STAR, color=ft.colors.YELLOW, size=18),
                                                ft.Icon(name=ft.icons.STAR, color=ft.colors.YELLOW, size=18),
                                                ft.Icon(name=ft.icons.STAR, color=ft.colors.YELLOW, size=18),
                                                ft.Icon(name=ft.icons.STAR, color=ft.colors.YELLOW, size=18),
                                                ft.Icon(name=ft.icons.STAR, color=ft.colors.YELLOW, size=18),
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

def generate_specialist_column(page):
    return ft.Column(
        controls=[
            generate_header(page),
            generate_worker_row_column("@sn3g0v1k20 \"GenZGuy\"", "тренер по прыжкам с крыши", f"/specialist1.jpg", "87 отзывов"),
            generate_worker_row_column("@sn3g0v1k20 Aurudin", "тренер по гандболу", f"/specialist1.jpg",
                                       "1 отзывов")

        ],
        spacing=10,
        scroll=ft.ScrollMode.ADAPTIVE
    )
