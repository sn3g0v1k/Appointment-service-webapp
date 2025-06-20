import flet as ft
import datetime

from webapp.database import get_time_on_date
from icecream import ic

from .settings import plogo


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
                    gen_text("Выбрать время", 24, ft.FontWeight.BOLD),
                ],
                spacing=0,
            )
        ],
        alignment=ft.MainAxisAlignment.START,
    )

def time_picked(time, date, page):
    page.session.set("nametimedate", (page.session.get("employee_name"), time, date))
    ic((page.session.get("employee_name"), time, date))
    page.go("/choose_service")

def generate_time_grid(data: list, date, page):
    ic(data)
    grid = ft.GridView(
        expand=1,
        runs_count=3,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10,
    )
    
    for time_slot in data:
        grid.controls.append(
            ft.Container(
                content=ft.ElevatedButton(
                    text=time_slot[0],
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLUE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    on_click=lambda _, t=time_slot[0]: time_picked(t, date, page)
                ),
                padding=5,
            )
        )
    
    return grid

def handle_change(e, page):
    date = e.control.value.strftime('%d.%m.%Y')
    name = page.session.get("employee_name")
    time = get_time_on_date(date, name)
    
    if len(time) == 0:
        content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.INFO_OUTLINE, size=50, color=ft.colors.ORANGE),
                gen_text(
                    "В этот день нет подходящего свободного времени,\nпопробуйте выбрать другую дату.",
                    20,
                    color=ft.colors.ORANGE
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        padding=20,
        bgcolor=ft.colors.ORANGE_50,
        border_radius=10,
        margin=ft.margin.only(top=20)
        )
    else:
        content = ft.Container(
            content=ft.Column([
                gen_text(f"Доступное время на {date}:", 20, ft.FontWeight.BOLD),
                generate_time_grid(time, date, page)
            ],
            spacing=20
        ),
        padding=20
        )
    
    page.views[-1].controls[0].content.controls[-1] = content
    page.update()

def generate_datepicker(page):
    return ft.DatePicker(
        first_date=datetime.datetime(year=2024, month=10, day=1),
        last_date=datetime.datetime(year=2026, month=10, day=1),
        on_change=lambda e: handle_change(e, page),
    )

def generate_ctime_column(page):
    return ft.Column(
        controls=[
            generate_header(page),
            ft.Container(
                content=ft.ElevatedButton(
                    text="Выбрать дату",
                    icon=ft.icons.CALENDAR_MONTH,
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLUE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    on_click=lambda e: page.open(generate_datepicker(page))
                ),
                padding=20,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column([
                    gen_text("Выберите удобное время:", 20, ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text("Нажмите на кнопку выше, чтобы выбрать дату"),
                        padding=20,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=10,
                        alignment=ft.alignment.center
                    )
                ],
                spacing=20
                ),
                padding=20
            )
        ]
    )