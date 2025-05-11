import flet as ft

from webapp.main_w import main

ft.app(main, view=ft.WEB_BROWSER, port=5000)  # asd , assets_dir="webapp/assets"
# flet run -d -r -w -p 5000 -a webapp/assets start_webapp.py