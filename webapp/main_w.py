import flet as ft
from icecream import ic

from .indexpage import generate_index_column
from .infopage import generate_info_column
from .choose_specialist import generate_specialist_column
from .choose_time import generate_ctime_column
from .choose_service import generate_service_column
from .settings import bgcolor
from .profile import generate_profile_column


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

    def create_appbar(nickname: str = "UserNick", avatar_url: str = "https://picsum.photos/id/1005/200/300"):
        return ft.AppBar(
            leading=None,  # Скрываем стандартный leading
            title=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src=avatar_url,
                            width=40,
                            height=40,
                            fit=ft.ImageFit.COVER,
                        ),
                        width=40,
                        height=40,
                        border_radius=20,  # Круглый аватар
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    ),
                    ft.Text(
                        nickname,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=12,
            ),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            elevation=4,  # Легкая тень для современного вида
            actions=[],
            toolbar_height=60,  # Увеличиваем высоту для лучшего восприятия
        )
    page.appbar = create_appbar()
    page.update()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Container(
                        content=generate_index_column(page),
                        expand=True,
                        bgcolor=bgcolor
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                        bgcolor=bgcolor
            )
        )
        ic(page.route)
        try:
            tg_id = page.route.split("=")[1]
            page.session.set("user_id", int(tg_id))
        except:
            pass
        if page.route == "/info":
            page.views.append(
                ft.View(
                    "/info",
                    [
                        ft.Container(
                            content=generate_info_column(page),
                            expand=True,
                        bgcolor=bgcolor
                        )
                    ],
                scroll=ft.ScrollMode.ADAPTIVE,
                        bgcolor=bgcolor
                )
            )
        elif page.route == "/profile":
            page.views.append(
                ft.View(
                    "/profile",
                    [
                        ft.Container(
                            content=generate_profile_column(page),
                            expand=True,
                        bgcolor=bgcolor
                        )
                    ],
                scroll=ft.ScrollMode.ADAPTIVE,
                        bgcolor=bgcolor
                )
            )
        elif page.route == "/choose_specialist":
            page.views.append(
                ft.View(
                    "/choose_specialist",
                    [
                        ft.Container(
                            content=generate_specialist_column(page),
                            expand=True,
                        bgcolor=bgcolor
                        )
                    ],
                scroll=ft.ScrollMode.ADAPTIVE,
                        bgcolor=bgcolor
                )
            )
        elif page.route == "/choose_time":
            page.views.append(
                ft.View(
                    "/choose_time",
                    [
                        ft.Container(
                            content=generate_ctime_column(page),
                            expand=True,
                        bgcolor=bgcolor
                        )
                    ],
                scroll=ft.ScrollMode.ADAPTIVE,
                        bgcolor=bgcolor
                )
            )
        elif page.route == "/choose_service":
            page.views.append(
                ft.View(
                    "/choose_service",
                    [
                        ft.Container(
                            content=generate_service_column(page),
                            expand=True,
                        bgcolor=bgcolor
                        )
                    ],
                scroll=ft.ScrollMode.ADAPTIVE,
                        bgcolor=bgcolor
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


