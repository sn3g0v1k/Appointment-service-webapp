import flet as ft

schedule_today = ft.Container(

    content=ft.Column(

        [

            ft.Text("РАСПИСАНИЕ НА СЕГОДНЯ", size=16, weight=ft.FontWeight.BOLD),

            ft.Text(f"{get_current_date()}", size=14),

            ft.Container(

                content=create_schedule_content(todays_trainings),

                padding=ft.padding.all(10),

                bgcolor=ft.Colors.WHITE,

                border_radius=10,

                expand=True,

            ),

        ],

        alignment=ft.MainAxisAlignment.CENTER,

        spacing=2,

    ),

    alignment=ft.alignment.center,

    width=500,

    height=335,

    #bgcolor=ft.Colors.WHITE,

    #border=ft.border.all(1, ft.Colors.BLACK),

    border_radius=15,

    padding=5,

)







def create_schedule_content(todays_trainings):

    if not todays_trainings:

        return ft.Column(

            controls=[

                ft.Text("На сегодня нет тренировок", size=14, color=ft.Colors.GREY),

            ],

            scroll=ft.ScrollMode.AUTO,

            spacing=10,

        )



    schedule_items = []

    for training in todays_trainings:

        if not isinstance(training, dict):

            continue



        service_title = training.get('Service', {}).get('Title', 'Не указано')

        start_date = training.get('StartDate', None)

        if start_date:

            start_time = datetime.strptime(start_date, "%Y-%m-%d %H:%M").strftime('%H:%M')

        else:

            start_time = 'Не указано'

        duration = training.get('Duration', 'Не указано')

        available_slots = training.get('AvailableSlots', 'Не указано')

        if available_slots == 'Unlimited':

            available_slots = 'Неограничено'

        trainer_name = training.get('Employee', {}).get('FullName', '-')

        if isinstance(trainer_name, str) and '(' in trainer_name:

            trainer_name = trainer_name.split('(')[0].strip()

        divider_color = training.get('Service', {}).get('Color', '#000000')



        info_container = ft.Container(

            content=ft.Column(

                controls=[

                    ft.Text(

                        service_title,

                        size=14,

                        weight=ft.FontWeight.BOLD,

                        color=ft.Colors.BLACK

                    ),

                    ft.Text(f"📍 {training['Room']['Title']}", size=10),

                    ft.Text(

                        f"Свободно: {available_slots} мест\n"

                        f"{trainer_name}",

                        size=10,

                        color=ft.Colors.GREY_700,

                    ),

                ],

                spacing=5

            ),

            padding=ft.padding.symmetric(vertical=2, horizontal=12),

            margin=ft.margin.only(left=10),

            alignment=ft.alignment.center_left

        )



        time_container = ft.Container(

            content=ft.Column(

                controls=[

                    ft.Text(

                        start_time,

                        size=14,

                        weight=ft.FontWeight.BOLD,

                        color=ft.Colors.BLACK

                    ),

                    ft.Text(

                        f"{duration} мин",

                        size=10,

                        color=ft.Colors.GREY_700

                    )

                ],

                spacing=5

            ),

            padding=ft.padding.symmetric(vertical=2),

            margin=ft.margin.only(right=10),

            alignment=ft.alignment.center_right

        )



        divider_container = ft.Container(

            width=5,

            height=40,

            bgcolor=divider_color,

            border_radius=ft.border_radius.all(2),

            margin=ft.margin.symmetric(vertical=4)

        )



        schedule_row = ft.Row(

            controls=[

                time_container,

                divider_container,

                info_container

            ],

            spacing=0,

            alignment=ft.MainAxisAlignment.START,

            vertical_alignment=ft.CrossAxisAlignment.CENTER

        )



        schedule_items.append(schedule_row)



        if training != todays_trainings[-1]:

            schedule_items.append(

                ft.Divider(

                    color=ft.Colors.GREY_400,

                    thickness=1,

                    height=20

                )

            )



    return ft.Column(

        controls=schedule_items,

        scroll=ft.ScrollMode.AUTO,

        spacing=2,

    )

