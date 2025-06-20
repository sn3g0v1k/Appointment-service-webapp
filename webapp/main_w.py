import flet as ft
from icecream import ic
import logging

from .indexpage import generate_index_column
from .infopage import generate_info_column
from .choose_specialist import generate_specialist_column
from .choose_time import generate_ctime_column
from .choose_service import generate_service_column
from .settings import bgcolor
from .profile import generate_profile_column

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='webapp.log'
)
logger = logging.getLogger(__name__)

def get_switcher(view):
    return ft.AnimatedSwitcher(
        content=view,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=300,  # Увеличиваем длительность анимации
        reverse_duration=300,
        switch_in_curve=ft.AnimationCurve.BOUNCE_IN,
        switch_out_curve=ft.AnimationCurve.BOUNCE_OUT,
    )



def main(page: ft.Page):
    try:
        page.title = "Система записи к специалистам"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.SYSTEM  # Поддержка системной темы

        # Настройка шрифтов
        page.fonts = {
            "Caveat": "https://github.com/sn3g0v1k/veryfont/raw/refs/heads/main/Caveat-VariableFont_wght.ttf",
            "Roboto": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf"
        }
        page.theme = ft.Theme(
            font_family="Roboto",
            color_scheme_seed=ft.colors.BLUE,
        )
        page.scroll = ft.ScrollMode.ADAPTIVE

        def create_appbar(nickname: str = "UserNick", avatar_url: str = "https://picsum.photos/id/1005/200/300"):
            return ft.AppBar(
                leading=None,
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
                            border_radius=20,
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
                elevation=4,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.DARK_MODE,
                        on_click=lambda e: toggle_theme(e),
                        tooltip="Сменить тему"
                    ),
                ],
                toolbar_height=60,
            )

        def toggle_theme(e):
            page.theme_mode = (
                ft.ThemeMode.DARK
                if page.theme_mode == ft.ThemeMode.LIGHT
                else ft.ThemeMode.LIGHT
            )
            page.update()

        page.appbar = create_appbar()
        page.update()

        def route_change(route):

            ic(page.route)
            if page.route.startswith("/?tg_id="):
                try:
                    tg_id = page.route.split("=")[1]
                except:
                    tg_id = 123
                    ic(f"Не удалось получить tg_id из route: {page.route}")
                ic(tg_id)
                page.session.set("user_id", int(tg_id))
            # try:
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



            routes = {
                "/info": generate_info_column,
                "/profile": generate_profile_column,
                "/choose_specialist": generate_specialist_column,
                "/choose_time": generate_ctime_column,
                "/choose_service": generate_service_column,
            }

            if page.route in routes:
                page.views.append(
                    ft.View(
                        page.route,
                        [
                            ft.Container(
                                content=routes[page.route](page),
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

            # except Exception as e:
            #     logger.error(f"Ошибка при смене маршрута: {str(e)}")
            #     page.show_snack_bar(
            #         ft.SnackBar(
            #             content=ft.Text("Произошла ошибка при загрузке страницы"),
            #             bgcolor=ft.colors.RED_400,
            #         )
            #     )

        def view_pop(view):
            try:
                page.views.pop()
                top_view = page.views[-1]
                page.go(top_view.route)
            except Exception as e:
                logger.error(f"Ошибка при возврате на предыдущую страницу: {str(e)}")
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Произошла ошибка при возврате на предыдущую страницу"),
                        bgcolor=ft.colors.RED_400,
                    )
                )

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)

    except Exception as e:
        logger.error(f"Критическая ошибка в приложении: {str(e)}")
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Произошла критическая ошибка в приложении"),
                bgcolor=ft.colors.RED_400,
            )
        )


