from pathlib import Path

import streamlit as st

CSS_FILE = (
    Path(__file__).parent.parent
    / "assets"
    / "styles.css"
)


def load_css() -> None:
    """Load the dashboard stylesheet."""

    st.markdown(
        f"<style>{CSS_FILE.read_text()}</style>",
        unsafe_allow_html=True,
    )