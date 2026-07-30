from pathlib import Path

import plotly.graph_objects as go
import streamlit as st


def vertical_spacer(size: str = "1rem") -> None:
    st.markdown(
        f"<div style='height: {size};'></div>",
        unsafe_allow_html=True,
    )


def metric_card(
    title: str,
    value: str | int | float,
    *,
    help: str | None = None,
) -> None:
    """Display a dashboard metric card."""

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
            help=help,
        )


def chart_card(
    title: str,
    figure: go.Figure,
) -> None:
    """Display a chart inside a dashboard card."""

    with st.container(border=True):

        st.markdown(
            f"""
            <div class="chart-title">
                {title}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
            config={"displayModeBar": False},
        )


def info_card(
    icon: str,
    title: str,
    value: str,
) -> None:
    """Display a dashboard insight."""

    with st.container(border=True):
        st.markdown(f"""
            <div class="info-title">
                <h3>{icon} {title}</h3>
            </div>
            """, unsafe_allow_html=True)
        st.write(value)


def navigation_card(
    title: str,
    icon: str,
    description: str,
    page: str | Path,
) -> None:
    """Display a navigation card linking to another dashboard page."""

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="navigation-card">
                <div class="navigation-title">
                    <h3>{icon} {title}</h3>
                </div>
                <div class="navigation-description">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            f"Open {title} →",
            use_container_width=True,
            key=f"nav_{title}",
        ):
            st.switch_page(page)