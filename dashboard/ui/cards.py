from contextlib import contextmanager
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.data.profile import UniversityProfile
from dashboard.visualization.charts import map_preview


def vertical_spacer(size: str = "1rem") -> None:
    """Add a vertical spacer of the specified size."""

    st.markdown(
        f"<div style='height: {size};'></div>",
        unsafe_allow_html=True,
    )


def page_header(title: str, description: str | None = None) -> None:
    """Display a page header with an optional description."""

    st.title(title)
    if description:
        st.write(description)

    vertical_spacer()


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


def map_preview_card(institutions_df: pd.DataFrame) -> None:
    """Render the overview world map preview."""

    with st.container(border=True):
        st.subheader("🌍 University Destinations")
        st.caption(
            "Preview of university destinations. "
            "Open the interactive map to explore individual universities."
        )

        fig = map_preview(institutions_df)

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False,
                "staticPlot": True,
            },
        )

        if st.button(
            "🌍 Explore Interactive Map",
            key="explore_map",
            width="stretch",
        ):
            st.switch_page("pages/02_World_Map.py")


def chart_card(
    title: str,
    figure: go.Figure,
) -> None:
    """Display a chart inside a dashboard card."""

    with st.container(border=True):
        st.subheader(title)

        st.plotly_chart(
            figure,
            width="stretch",
            config={"displayModeBar": False},
        )


@contextmanager
def primary_section(
    title: str,
    description: str,
):
    """Display a primary visualization card."""

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="primary-chart">
                <h2>{title}</h2>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        yield


def info_card(
    icon: str,
    title: str,
    value: str,
) -> None:
    """Display a dashboard insight."""

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="info-title">
                <h3>{icon} {title}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
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
            width="stretch",
            key=f"nav_{title}",
        ):
            st.switch_page(page)


def university_profile_card(
    profile: UniversityProfile,
) -> None:
    """Display a profile card for the selected university."""

    with st.container(border=True):
        st.subheader("University Profile")

        st.markdown(
            f"""
            <div class="profile-content">
            <div class="profile-row">
                <span class="profile-label">University</span>
                <span class="profile-value">{profile.institution}</span>
            </div>

            <div class="profile-row">
                <span class="profile-label">Country</span>
                <span class="profile-value">{profile.country}</span>
            </div>

            <div class="profile-row">
                <span class="profile-label">Students</span>
                <span class="profile-value">{profile.students}</span>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
