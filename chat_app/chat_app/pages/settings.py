"""The settings page."""

from chat_app.templates import ThemeState, template

import reflex as rx


@template(route="/settings", title="Reports")
def settings() -> rx.Component:
    """The settings page.

    Returns:
        The UI for the settings page.
    """
    return rx.vstack(
        rx.heading("Reports", size="8"),
        rx.text(
            "See your weekly summaries here!",
        ),
    )
