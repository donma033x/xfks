import reflex as rx
from app.components.entry_form import entry_form
from app.components.account_table import account_table
from app.components.log_panel import log_panel
from app.components.stats_cards import stats_row


def header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("cpu", class_name="w-8 h-8 text-emerald-600 mr-3"),
            rx.el.h1(
                "Batch Auto-Learn",
                class_name="text-2xl font-bold text-gray-900 tracking-tight",
            ),
            rx.el.span(
                "Platform", class_name="text-2xl font-light text-emerald-600 ml-1"
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("bell", class_name="w-5 h-5 text-gray-600"),
                class_name="p-2 rounded-full hover:bg-gray-100 transition-colors relative",
            ),
            rx.el.div(class_name="w-px h-6 bg-gray-200 mx-2"),
            rx.el.div(
                rx.el.span(
                    "Admin", class_name="text-sm font-medium text-gray-700 mr-2"
                ),
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=Admin",
                    class_name="w-8 h-8 rounded-full bg-emerald-100",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex justify-between items-center py-6 px-2",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.p(
                "© 2024 Batch Auto-Learn Platform. All rights reserved.",
                class_name="text-sm text-gray-500 text-center",
            ),
            class_name="py-8 border-t border-gray-100 mt-8",
        ),
        class_name="w-full",
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            header(),
            rx.el.div(
                stats_row(),
                rx.el.div(
                    rx.el.div(
                        entry_form(),
                        class_name="w-full lg:w-[350px] xl:w-[380px] shrink-0",
                    ),
                    rx.el.div(
                        account_table(),
                        log_panel(),
                        class_name="flex-1 flex flex-col gap-6 min-w-0 w-full",
                    ),
                    class_name="flex flex-col lg:flex-row gap-6 items-start w-full",
                ),
                class_name="flex flex-col gap-8 pb-12 w-full",
            ),
            footer(),
            class_name="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 min-h-screen flex flex-col w-full",
        ),
        class_name="min-h-screen bg-[#FAFAFA] font-['Raleway'] selection:bg-emerald-100 selection:text-emerald-900",
    )


from app.states.main_state import MainState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&display=swap",
            rel="stylesheet",
        )
    ],
)
app.add_page(index, route="/", on_load=MainState.run_simulation)