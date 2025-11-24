import reflex as rx
from app.states.main_state import MainState, Account


def status_badge(status: str, account_id: str) -> rx.Component:
    return rx.el.button(
        rx.match(
            status,
            (
                "Passed",
                rx.el.div(
                    rx.icon(
                        "check_check",
                        class_name="w-3 h-3 sm:w-4 sm:h-4 mr-0.5 sm:mr-1.5",
                    ),
                    rx.el.span("Pass", class_name="sm:hidden"),
                    rx.el.span("Passed", class_name="hidden sm:inline"),
                    class_name="inline-flex items-center px-1.5 py-0.5 sm:px-2.5 rounded-full text-[10px] sm:text-xs font-medium bg-emerald-100 text-emerald-800",
                ),
            ),
            (
                "Failed",
                rx.el.div(
                    rx.icon(
                        "circle_x", class_name="w-3 h-3 sm:w-4 sm:h-4 mr-0.5 sm:mr-1.5"
                    ),
                    rx.el.span("Fail", class_name="sm:hidden"),
                    rx.el.span("Failed", class_name="hidden sm:inline"),
                    class_name="inline-flex items-center px-1.5 py-0.5 sm:px-2.5 rounded-full text-[10px] sm:text-xs font-medium bg-red-100 text-red-800",
                ),
            ),
            (
                "Not Participating",
                rx.el.div(
                    rx.icon("ban", class_name="w-3 h-3 sm:w-4 sm:h-4 mr-0.5 sm:mr-1.5"),
                    "N/A",
                    class_name="inline-flex items-center px-1.5 py-0.5 sm:px-2.5 rounded-full text-[10px] sm:text-xs font-medium bg-gray-100 text-gray-400",
                ),
            ),
            rx.el.div(
                rx.icon("circle", class_name="w-3 h-3 sm:w-4 sm:h-4 mr-0.5 sm:mr-1.5"),
                status,
                class_name="inline-flex items-center px-1.5 py-0.5 sm:px-2.5 rounded-full text-[10px] sm:text-xs font-medium bg-amber-100 text-amber-800",
            ),
        ),
        on_click=lambda: MainState.toggle_exam_status_in_table(account_id),
        disabled=status == "Passed",
        class_name=rx.cond(
            status == "Passed",
            "focus:outline-none cursor-default opacity-80",
            "focus:outline-none active:scale-95 transition-transform cursor-pointer hover:opacity-80",
        ),
        title=rx.cond(status == "Passed", "Exam Passed", "Click to cycle status"),
    )


def progress_bar(value: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="h-full bg-gradient-to-r from-emerald-400 to-emerald-600 rounded-full transition-all duration-700 ease-out shadow-[0_0_10px_rgba(16,185,129,0.3)]",
            style={"width": f"{value}%"},
        ),
        class_name="w-full h-1.5 sm:h-2 bg-gray-100 rounded-full overflow-hidden",
    )


def account_row(account: Account) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    account["username"],
                    class_name="font-medium text-gray-900 text-xs sm:text-sm",
                ),
                class_name="flex items-center",
            ),
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap",
        ),
        rx.el.td(
            account["name"],
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap text-gray-600 text-[10px] sm:text-sm",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"{account['study_progress']}%",
                        class_name="text-[10px] sm:text-xs font-semibold text-emerald-700",
                    ),
                    class_name="flex justify-end mb-1",
                ),
                progress_bar(account["study_progress"]),
                class_name="w-16 sm:w-32",
            ),
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge(account["exam_status"], account["id"]),
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        account["is_running"],
                        rx.icon("pause", class_name="w-3.5 h-3.5 sm:w-4 sm:h-4"),
                        rx.icon("play", class_name="w-3.5 h-3.5 sm:w-4 sm:h-4"),
                    ),
                    on_click=lambda: MainState.toggle_task_status(account["id"]),
                    class_name=rx.cond(
                        account["is_running"],
                        "p-1.5 sm:p-2 text-amber-600 hover:bg-amber-50 rounded-lg transition-colors",
                        "p-1.5 sm:p-2 text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors",
                    ),
                    title=rx.cond(account["is_running"], "Pause Task", "Start Task"),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-3.5 h-3.5 sm:w-4 sm:h-4"),
                    on_click=lambda: MainState.delete_account(account["id"]),
                    class_name="p-1.5 sm:p-2 text-red-400 hover:bg-red-50 rounded-lg transition-colors",
                    title="Delete",
                ),
                class_name="flex gap-1 sm:gap-2",
            ),
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        on_click=lambda: MainState.select_account(account["id"]),
        class_name=rx.cond(
            MainState.selected_account_id == account["id"],
            "bg-emerald-50/60 border-b border-emerald-100 last:border-0 cursor-pointer",
            "hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0 cursor-pointer",
        ),
    )


def completed_account_row(account: Account) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    account["username"],
                    class_name="font-medium text-gray-900 text-xs sm:text-sm",
                ),
                class_name="flex items-center",
            ),
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap",
        ),
        rx.el.td(
            account["name"],
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap text-gray-600 text-[10px] sm:text-sm",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "100%",
                        class_name="text-[10px] sm:text-xs font-semibold text-emerald-700",
                    ),
                    class_name="flex justify-end mb-1",
                ),
                progress_bar(100),
                class_name="w-16 sm:w-32",
            ),
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge("Passed", account["id"]),
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="w-3.5 h-3.5 sm:w-4 sm:h-4"),
                    on_click=lambda: MainState.refresh_account(account["id"]),
                    class_name="p-1.5 sm:p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
                    title="Refresh & Restart",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-3.5 h-3.5 sm:w-4 sm:h-4"),
                    on_click=lambda: MainState.delete_account(account["id"]),
                    class_name="p-1.5 sm:p-2 text-red-400 hover:bg-red-50 rounded-lg transition-colors",
                    title="Delete",
                ),
                class_name="flex gap-1 sm:gap-2 justify-end",
            ),
            class_name="px-2 py-3 sm:px-6 sm:py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        on_click=lambda: MainState.select_account(account["id"]),
        class_name=rx.cond(
            MainState.selected_account_id == account["id"],
            "bg-emerald-50/60 border-b border-emerald-100 last:border-0 cursor-pointer opacity-70",
            "hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0 cursor-pointer opacity-70",
        ),
    )


def empty_state() -> rx.Component:
    return rx.el.div(
        rx.icon("users", class_name="w-12 h-12 sm:w-16 sm:h-16 text-gray-200 mb-4"),
        rx.el.h3(
            "No Accounts Active",
            class_name="text-base sm:text-lg font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Add an account to start the automated learning process.",
            class_name="text-gray-500 text-center max-w-xs text-sm sm:text-base",
        ),
        class_name="flex flex-col items-center justify-center h-56 sm:h-64 p-4 sm:p-8",
    )


def render_table(accounts: list[Account], row_renderer: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Account",
                        class_name="px-2 py-3 sm:px-6 sm:py-4 text-left text-[10px] sm:text-xs font-bold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Name",
                        class_name="px-2 py-3 sm:px-6 sm:py-4 text-left text-[10px] sm:text-xs font-bold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Progress",
                        class_name="px-2 py-3 sm:px-6 sm:py-4 text-left text-[10px] sm:text-xs font-bold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Status",
                        class_name="px-2 py-3 sm:px-6 sm:py-4 text-left text-[10px] sm:text-xs font-bold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Actions",
                        class_name="px-2 py-3 sm:px-6 sm:py-4 text-right text-[10px] sm:text-xs font-bold text-gray-500 uppercase tracking-wider",
                    ),
                ),
                class_name="bg-gray-50/50 border-b border-gray-100",
            ),
            rx.el.tbody(
                rx.foreach(accounts, row_renderer),
                class_name="divide-y divide-gray-100 bg-white",
            ),
            class_name="min-w-full",
        ),
        class_name="overflow-x-auto",
    )


def completed_section() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon("check_check", class_name="w-5 h-5 text-emerald-600 mr-2"),
                rx.el.span(
                    f"Completed Accounts ({MainState.completed_count})",
                    class_name="font-medium text-gray-700",
                ),
                class_name="flex items-center",
            ),
            rx.icon(
                "chevron-down",
                class_name=rx.cond(
                    MainState.show_completed,
                    "w-5 h-5 text-gray-400 transform rotate-180 transition-transform",
                    "w-5 h-5 text-gray-400 transition-transform",
                ),
            ),
            on_click=MainState.toggle_show_completed,
            class_name="w-full flex items-center justify-between p-4 bg-gray-50/50 hover:bg-gray-50 transition-colors border-t border-gray-100",
        ),
        rx.cond(
            MainState.show_completed,
            rx.el.div(
                render_table(MainState.completed_accounts, completed_account_row),
                class_name="border-t border-gray-100 animate-in fade-in slide-in-from-top-2",
            ),
        ),
        class_name="w-full",
    )


def account_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Monitoring Queue",
                class_name="text-xl font-semibold text-gray-800 mb-6 px-6 pt-6",
            ),
            rx.cond(
                MainState.accounts,
                rx.el.div(
                    render_table(MainState.active_accounts, account_row),
                    rx.cond(MainState.completed_count > 0, completed_section()),
                    class_name="w-full",
                ),
                empty_state(),
            ),
            class_name="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden flex flex-col w-full",
        ),
        class_name="w-full min-w-0",
    )