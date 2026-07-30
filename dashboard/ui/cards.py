import plotly.graph_objects as go
import streamlit as st


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
                <h5>{icon} {title}</h5>
            </div>
            """, unsafe_allow_html=True)
        st.write(value)