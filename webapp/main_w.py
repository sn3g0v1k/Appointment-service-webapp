import flet as ft
from indexpage import generate_index_column
from infopage import generate_info_column
from choose_specialist import generate_specialist_column

def get_switcher(view):
    return ft.AnimatedSwitcher(

        content=view,

        transition=ft.AnimatedSwitcherTransition.SCALE,

        duration=0,

        reverse_duration=0,

        switch_in_curve=ft.AnimationCurve.BOUNCE_IN,

        switch_out_curve=ft.AnimationCurve.BOUNCE_OUT,

    )


def main(page: ft.Page):
    page.title = "How did you get here? Text: @sn3g0v1k20 at telegram"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.fonts = {
        "Caveat": "https://github.com/sn3g0v1k/veryfont/raw/refs/heads/main/Caveat-VariableFont_wght.ttf"
    }
    page.theme = ft.Theme(font_family="Caveat")  # Default app font
    page.scroll = ft.ScrollMode.ADAPTIVE

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Container(
                        content=generate_index_column(page),
                        expand=True
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )

        if page.route == "/info":
            page.views.append(
                ft.View(
                    "/info",
                    [
                        ft.Container(
                            content=generate_info_column(page),
                            expand=True
                        )
                    ],
                scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        elif page.route == "/choose_specialist":
            page.views.append(
                ft.View(
                    "/choose_specialist",
                    [
                        ft.Container(
                            content=generate_specialist_column(page),
                            expand=True
                        )
                    ],
                scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        page.add(get_switcher(page.views[0]))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main, view=ft.WEB_BROWSER)  # asd , port=5000
