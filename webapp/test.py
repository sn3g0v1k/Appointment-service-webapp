import random
import flet as ft
import flet.map as map


def gen_map(page: ft.Page):
    m = map.Map(
            expand=True,
            initial_center=map.MapLatitudeLongitude(54.732927, 55.923271),
            initial_zoom=18,
            interaction_configuration=map.MapInteractionConfiguration(
                flags=map.MapInteractiveFlag.ALL
            ),
            layers=[
                map.TileLayer(
                    url_template="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
                ),
                map.RichAttribution(
                    attributions=[
                        map.TextSourceAttribution(
                            text="OpenStreetMap Contributors",
                            on_click=lambda e: e.page.launch_url(
                                "https://openstreetmap.org/copyright"
                            ),
                        ),
                        map.TextSourceAttribution(
                            text="Flet",
                            on_click=lambda e: e.page.launch_url("https://flet.dev"),
                        ),
                    ]
                ),
                map.SimpleAttribution(
                    text="Flet",
                    alignment=ft.alignment.top_right,
                ),
            ],

        )

    page.add(
        m
    )
    page.update()
    return m




