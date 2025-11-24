import reflex as rx
from typing import TypedDict, Optional
import datetime
import asyncio
import random


class Account(TypedDict):
    id: str
    username: str
    password: str
    name: str
    study_progress: int
    exam_status: str
    study_selected: bool
    exam_selected: bool
    is_running: bool


class LogEntry(TypedDict):
    id: int
    account_id: Optional[str]
    time: str
    message: str
    level: str


class MainState(rx.State):
    form_username: str = ""
    form_password: str = ""
    form_is_study: bool = True
    form_is_exam: bool = False
    is_verifying: bool = False
    selected_account_id: str | None = None
    accounts: list[Account] = [
        {
            "id": "1",
            "username": "student001",
            "password": "***",
            "name": "Alice Zhang",
            "study_progress": 45,
            "exam_status": "Pending",
            "study_selected": True,
            "exam_selected": True,
            "is_running": True,
        },
        {
            "id": "2",
            "username": "student002",
            "password": "***",
            "name": "Bob Chen",
            "study_progress": 100,
            "exam_status": "Passed",
            "study_selected": True,
            "exam_selected": False,
            "is_running": False,
        },
        {
            "id": "3",
            "username": "student003",
            "password": "***",
            "name": "Charlie Wu",
            "study_progress": 12,
            "exam_status": "Failed",
            "study_selected": False,
            "exam_selected": True,
            "is_running": False,
        },
    ]
    logs: list[LogEntry] = [
        {
            "id": 1,
            "account_id": None,
            "time": "10:00:01",
            "message": "System initialized successfully",
            "level": "info",
        },
        {
            "id": 2,
            "account_id": "1",
            "time": "10:05:23",
            "message": "Added student001 to queue",
            "level": "success",
        },
        {
            "id": 3,
            "account_id": "3",
            "time": "10:15:00",
            "message": "Connection timeout for student003",
            "level": "error",
        },
    ]

    @rx.var
    def filtered_logs(self) -> list[LogEntry]:
        if self.selected_account_id is None:
            return self.logs
        return [
            log
            for log in self.logs
            if log.get("account_id") == self.selected_account_id
            or log.get("account_id") is None
        ]

    @rx.var
    def total_accounts_count(self) -> int:
        return len(self.accounts)

    @rx.var
    def running_tasks_count(self) -> int:
        return len([a for a in self.accounts if a["is_running"]])

    show_completed: bool = False

    @rx.var
    def average_progress(self) -> int:
        if not self.accounts:
            return 0
        total = sum((a["study_progress"] for a in self.accounts))
        return int(total / len(self.accounts))

    @rx.var
    def active_accounts(self) -> list[Account]:
        return [
            a
            for a in self.accounts
            if not (a["study_progress"] == 100 and a["exam_status"] == "Passed")
        ]

    @rx.var
    def completed_accounts(self) -> list[Account]:
        return [
            a
            for a in self.accounts
            if a["study_progress"] == 100 and a["exam_status"] == "Passed"
        ]

    @rx.var
    def completed_count(self) -> int:
        return len(self.completed_accounts)

    @rx.event
    def toggle_show_completed(self):
        self.show_completed = not self.show_completed

    @rx.event
    def update_username(self, value: str):
        self.form_username = value

    @rx.event
    def update_password(self, value: str):
        self.form_password = value

    @rx.event
    def toggle_study(self, value: bool):
        self.form_is_study = value

    @rx.event
    def toggle_exam(self, value: bool):
        self.form_is_exam = value

    @rx.event
    def select_account(self, account_id: str):
        if self.selected_account_id == account_id:
            self.selected_account_id = None
        else:
            self.selected_account_id = account_id

    @rx.event
    async def add_account(self):
        if not self.form_username or not self.form_password:
            yield rx.toast.error("Please enter username and password")
            return
        if any((a["username"] == self.form_username for a in self.accounts)):
            yield rx.toast.error(f"Account {self.form_username} already exists")
            return
        self.is_verifying = True
        self.add_log(f"Starting verification for {self.form_username}...", "info", None)
        yield
        await asyncio.sleep(1.5)
        names = ["David Li", "Eva Wang", "Frank Zhao", "Grace Liu", "Henry Sun"]
        new_name = random.choice(names)
        new_id = str(len(self.accounts) + len(self.logs) + 100)
        exam_status_initial = "Pending" if self.form_is_exam else "Not Participating"
        new_account = {
            "id": new_id,
            "username": self.form_username,
            "password": "***",
            "name": new_name,
            "study_progress": 0,
            "exam_status": exam_status_initial,
            "study_selected": self.form_is_study,
            "exam_selected": self.form_is_exam,
            "is_running": True,
        }
        self.accounts.append(new_account)
        self.add_log(
            f"Verified and added account {self.form_username} as {new_name}",
            "success",
            new_id,
        )
        self.form_username = ""
        self.form_password = ""
        self.form_is_study = True
        self.form_is_exam = False
        self.is_verifying = False
        yield rx.toast.success(f"Account {new_name} added successfully")

    @rx.event
    def delete_account(self, account_id: str):
        account = next((a for a in self.accounts if a["id"] == account_id), None)
        if account:
            self.accounts = [a for a in self.accounts if a["id"] != account_id]
            self.add_log(f"Deleted account {account['username']}", "error", None)
            if self.selected_account_id == account_id:
                self.selected_account_id = None
            yield rx.toast.info(f"Account {account['username']} has been removed")

    @rx.event
    def toggle_task_status(self, account_id: str):
        for account in self.accounts:
            if account["id"] == account_id:
                account["is_running"] = not account["is_running"]
                status = "Started" if account["is_running"] else "Stopped"
                self.add_log(
                    f"{status} tasks for {account['username']}", "info", account_id
                )
                break

    @rx.event
    def toggle_exam_status_in_table(self, account_id: str):
        for account in self.accounts:
            if account["id"] == account_id:
                current = account["exam_status"]
                new_status = current
                if current == "Not Participating":
                    new_status = "Pending"
                elif current == "Pending":
                    new_status = "Passed"
                if new_status != current:
                    account["exam_status"] = new_status
                    self.add_log(
                        f"Manually changed exam status to {new_status} for {account['username']}",
                        "info",
                        account_id,
                    )
                break

    @rx.event
    def refresh_account(self, account_id: str):
        account = next((a for a in self.accounts if a["id"] == account_id), None)
        if account:
            account["study_progress"] = 0
            account["exam_status"] = (
                "Pending" if account["exam_selected"] else "Not Participating"
            )
            account["is_running"] = True
            self.logs = [
                log for log in self.logs if log.get("account_id") != account_id
            ]
            self.add_log(
                f"Account {account['username']} refreshed and restarted",
                "success",
                account_id,
            )

    @rx.event
    def add_log(self, message: str, level: str = "info", account_id: str | None = None):
        new_log = {
            "id": len(self.logs) + 1,
            "account_id": account_id,
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "message": message,
            "level": level,
        }
        self.logs.insert(0, new_log)

    @rx.event(background=True)
    async def run_simulation(self):
        while True:
            async with self:
                changes = False
                for account in self.accounts:
                    if account["is_running"] and account["study_progress"] < 100:
                        increment = random.choice([0, 1, 2, 5])
                        if increment > 0:
                            account["study_progress"] = min(
                                100, account["study_progress"] + increment
                            )
                            changes = True
                            if account["study_progress"] == 100:
                                self.add_log(
                                    f"Study completed for {account['username']}",
                                    "success",
                                    account["id"],
                                )
            await asyncio.sleep(1)