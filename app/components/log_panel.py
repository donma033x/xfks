import reflex as rx
from app.states.main_state import MainState, LogEntry


def log_item(log: LogEntry) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                log["time"],
                class_name="text-xs font-mono text-gray-400 mr-3 min-w-[55px] shrink-0",
            ),
            rx.el.div(
                rx.match(
                    log["level"],
                    (
                        "error",
                        rx.icon(
                            "badge_alert", class_name="w-3.5 h-3.5 text-red-500 mt-0.5"
                        ),
                    ),
                    (
                        "success",
                        rx.icon(
                            "square_check",
                            class_name="w-3.5 h-3.5 text-emerald-500 mt-0.5",
                        ),
                    ),
                    rx.icon("info", class_name="w-3.5 h-3.5 text-blue-400 mt-0.5"),
                ),
                class_name="mr-2 shrink-0",
            ),
            rx.el.span(
                log["message"],
                class_name=rx.match(
                    log["level"],
                    ("error", "text-red-700 font-medium"),
                    ("success", "text-emerald-700 font-medium"),
                    "text-gray-600",
                ),
            ),
            class_name="flex items-start text-sm",
        ),
        class_name="py-2.5 border-b border-gray-50 last:border-0 hover:bg-gray-50/50 px-2 -mx-2 rounded transition-colors",
    )


def log_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "System Logs", class_name="text-lg font-semibold text-gray-800"
                ),
                rx.cond(
                    MainState.selected_account_id,
                    rx.el.span(
                        "Filtered",
                        class_name="px-2 py-1 rounded bg-emerald-100 text-emerald-700 text-xs font-medium",
                    ),
                ),
                class_name="mb-4 flex items-center gap-2 justify-between",
            ),
            rx.el.div(
                rx.foreach(MainState.filtered_logs, log_item),
                class_name="overflow-y-auto max-h-[300px] lg:max-h-[400px] pr-2 custom-scrollbar space-y-1",
            ),
            class_name="p-6",
        ),
        class_name="bg-white rounded-3xl shadow-sm border border-gray-100 w-full overflow-hidden",
    )