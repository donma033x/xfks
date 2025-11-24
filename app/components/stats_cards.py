import reflex as rx
from app.states.main_state import MainState


def stat_item(
    icon: str, label: str, value: str, color: str, bg_color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-5 h-5 sm:w-6 sm:h-6 {color}"),
            class_name=f"p-2 sm:p-3 rounded-xl {bg_color} mb-1 sm:mb-2",
        ),
        rx.el.div(
            rx.el.p(
                value,
                class_name="text-lg sm:text-2xl font-bold text-gray-900 leading-tight mb-0.5",
            ),
            rx.el.p(
                label,
                class_name="text-[10px] sm:text-xs font-semibold text-gray-500 uppercase tracking-wider text-center",
            ),
            class_name="flex flex-col items-center",
        ),
        class_name="flex flex-col items-center justify-center flex-1 p-2 sm:p-4",
    )


def stats_row() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_item(
                "users",
                "Total",
                MainState.total_accounts_count.to_string(),
                "text-blue-600",
                "bg-blue-50",
            ),
            rx.el.div(class_name="w-px h-12 sm:h-16 bg-gray-100"),
            stat_item(
                "zap",
                "Running",
                MainState.running_tasks_count.to_string(),
                "text-amber-600",
                "bg-amber-50",
            ),
            rx.el.div(class_name="w-px h-12 sm:h-16 bg-gray-100"),
            stat_item(
                "bar-chart-3",
                "Progress",
                f"{MainState.average_progress}%",
                "text-emerald-600",
                "bg-emerald-50",
            ),
            class_name="flex flex-row justify-between items-center w-full gap-1 sm:gap-2",
        ),
        class_name="w-full bg-white rounded-3xl shadow-sm border border-gray-100 p-3 sm:p-4",
    )