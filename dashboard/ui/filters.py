import streamlit as st


def entity_selector(
    label: str,
    options: list[str],
) -> str:
    """Display a dropdown for selecting an entity."""

    return st.selectbox(
        label,
        sorted(options),
        index=None,
        placeholder=f"Select a {label.lower()}...",
        width="stretch",
    )