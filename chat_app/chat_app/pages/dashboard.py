"""The dashboard page."""

from chat_app.templates import template

import reflex as rx


@template(route="/dashboard", title="Tasks")
def dashboard() -> rx.Component:
    """The dashboard page.
re
    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Tasks", size="8"),
        # rx.text("Welcome to Reflex!"),
        # rx.text(
        #     "You can edit this page in ",
        #     rx.code("{your_app}/pages/Dashboard.py"),
        # ),
    )
