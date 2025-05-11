import flet as ft
import datetime

from flet.core.border_radius import horizontal

from database.database import get_time_on_date
from icecream import ic

from .settings import plogo


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
                    gen_text("Выбрать время", 20),
                ],
                spacing=0,
            )
        ],
        alignment=ft.MainAxisAlignment.START,
    )

def time_picked(time, date, page):
    page.session.set("nametimedate", (page.session.get("employee_name"), time, date))
    page.go("/choose_service")

def generate_table(data: list, date, page):
    ic(data)
    columns = [ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("") ),]
    rows = []
    hm_r = len(data)//3
    hm_cells_in_last_row = len(data) % 3
    for r in range(0, len(data)-hm_cells_in_last_row, 3):
        rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.ElevatedButton(text=data[r][0], on_click=lambda _, t=data[r][0]: time_picked(t, date, page))),
                        ft.DataCell(ft.ElevatedButton(data[r+1][0], on_click=lambda _, t=data[r+1][0]: time_picked(t, date, page))),
                        ft.DataCell(ft.ElevatedButton(text=data[r+2][0], on_click=lambda _, t=data[r+2][0]: time_picked(t, date, page))),
                    ],
                ))
    if hm_cells_in_last_row != 0:
        empty_cells = 3
        cells = []
        for r in range(hm_r*3, len(data)):

            cells.append(ft.DataCell(ft.ElevatedButton(text=data[r][0], on_click=lambda _, t = data[r][0]: time_picked(t, date, page))))
            empty_cells -= 1
        for i in range(empty_cells):
            cells.append(ft.DataCell(ft.Text("")))
        rows.append(ft.DataRow(cells=cells))
    return ft.DataTable(
            columns=columns,
            rows=rows,
        )

def handle_change(e, page):
    date = e.control.value.strftime('%d.%m.%Y')
    name = page.session.get("employee_name")
    time = get_time_on_date(date, name)
    if len(time) == 0:
        datatable = gen_text(text="В этот день нет подходящего свободного времени, \nпопробуйте выбрать другую дату.", size=20)
    else:
        datatable = generate_table(time, date, page)
    ic(page.views[-1].controls[0].content.controls[-1])
    page.views[-1].controls[0].content.controls[-1] = datatable
    page.update()
    ic(time)


def generate_datepicker(page):
    return ft.DatePicker(
                        first_date=datetime.datetime(year=2020, month=3, day=1),
                        last_date=datetime.datetime(year=2026, month=10, day=1),
                        on_change=lambda e: handle_change(e, page),
            )




def generate_ctime_column(page):
    return ft.Column(
        controls=[
            generate_header(page),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                    "Выбрать дату",
                    icon=ft.Icons.DATE_RANGE,
                    on_click=lambda e: page.open(
                        generate_datepicker(page)
                        ),
                    expand=True
                    ),
                ]
            ),
            ft.DataTable(columns=[ft.DataColumn(ft.Text(""))], rows=[])
        ]
    )