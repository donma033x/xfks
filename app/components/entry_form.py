import reflex as rx
from app.states.main_state import MainState


def entry_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Add Account",
                class_name="text-xl font-semibold text-gray-800 mb-6 flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Username / ID",
                            on_change=MainState.update_username,
                            class_name="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 text-gray-700 text-lg",
                            default_value=MainState.form_username,
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="password",
                            placeholder="Password",
                            on_change=MainState.update_password,
                            class_name="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 text-gray-700 text-lg",
                            default_value=MainState.form_password,
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex flex-col gap-5 w-full",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                checked=MainState.form_is_study,
                                on_change=MainState.toggle_study,
                                class_name="w-5 h-5 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500",
                            ),
                            rx.el.span(
                                "Study Task",
                                class_name="ml-3 text-gray-700 font-medium text-base",
                            ),
                            class_name="flex items-center cursor-pointer p-2 rounded-lg hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                checked=MainState.form_is_exam,
                                on_change=MainState.toggle_exam,
                                class_name="w-5 h-5 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500",
                            ),
                            rx.el.span(
                                "Exam Task",
                                class_name="ml-3 text-gray-700 font-medium text-base",
                            ),
                            class_name="flex items-center cursor-pointer p-2 rounded-lg hover:bg-gray-50 transition-colors",
                        ),
                        class_name="flex flex-col gap-1",
                    ),
                    rx.el.button(
                        rx.cond(
                            MainState.is_verifying,
                            rx.fragment(
                                rx.spinner(
                                    class_name="w-6 h-6 mr-2 text-white animate-spin"
                                ),
                                "Verifying...",
                            ),
                            rx.fragment(
                                rx.icon("plus", class_name="w-6 h-6 mr-2"),
                                "Verify & Add",
                            ),
                        ),
                        on_click=MainState.add_account,
                        disabled=MainState.is_verifying,
                        class_name=rx.cond(
                            MainState.is_verifying,
                            "flex items-center justify-center px-8 py-3.5 bg-emerald-400 text-white font-bold text-lg rounded-xl shadow-sm cursor-not-allowed w-full",
                            "flex items-center justify-center px-8 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-lg rounded-xl shadow-md hover:shadow-lg transition-all active:scale-95 w-full",
                        ),
                    ),
                    class_name="flex flex-col gap-6 mt-6 w-full",
                ),
                class_name="flex flex-col gap-2",
            ),
            class_name="p-6",
        ),
        class_name="bg-white rounded-3xl shadow-sm hover:shadow-lg transition-shadow duration-300 border border-gray-100 overflow-hidden",
    )