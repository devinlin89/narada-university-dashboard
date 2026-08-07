from collections.abc import Callable

import streamlit as st

from dashboard.ui.cards import metric_card


def two_column_layout(
    left_content: Callable[[], None],
    right_content: Callable[[], None],
) -> None:
    """Display two pieces of content side by side."""

    left, right = st.columns(2)

    with left:
        left_content()

    with right:
        right_content()


def metric_row(
    *metrics: tuple[str, str | int | float],
) -> None:
    """Display metrics in a single row."""

    columns = st.columns(len(metrics))

    for column, (label, value) in zip(columns, metrics):
        with column:
            metric_card(label, value)