from collections.abc import Callable

import streamlit as st


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