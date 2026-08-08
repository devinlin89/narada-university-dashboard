from textwrap import fill

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.config import REFERENCE_DATA
from dashboard.visualization.charts import (
    MAP_PREVIEW_HEIGHT,
    WORLD_MAP_HEIGHT,
)
from dashboard.visualization.flags import country_flag


def map_hover_text(
    institution: str,
    campus: str,
    country: str,
    student_count: int,
) -> str:
    """Create hover text for a university destination."""

    campus = (
        ""
        if campus == REFERENCE_DATA.default_values["campus"]
        else f"<br>📍 {campus}"
    )

    return (
        f"<b>🏛️ {(fill(
                institution,
                width=28
            )
            .replace('\n', '<br>')
        )}</b>"
        f"{campus}"
        f"<br>{country_flag(country)} {country}"
        f"<br>👨‍🎓 {student_count} "
        f"{'student' if student_count == 1 else 'students'}"
    )


def world_map(institutions_df: pd.DataFrame) -> go.Figure:
    """Create an interactive map of university destinations."""

    df = institutions_df.copy()

    df["hover"] = [
        map_hover_text(
            row.institution,
            row.campus,
            row.country,
            row.student_count,
        )
        for row in df.itertuples(index=False)
    ]

    df["marker_size"] = (
        2 + df["student_count"] ** 1.5 * 5
    )

    fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude",
        size="marker_size",
        custom_data=["hover"],
        height=WORLD_MAP_HEIGHT,
    )

    fig.update_traces(
        marker_color="#e2703e",
        marker_opacity=0.85,
        hovertemplate="%{customdata[0]}<extra></extra>",
    )

    fig.update_layout(
        map_style="carto-positron",
        map_center={
            "lat": df["latitude"].mean(),
            "lon": df["longitude"].mean(),
        },
        map_zoom=1.67,
        margin=dict(l=0, r=0, t=0, b=0),
        hoverlabel=dict(
            align="left",
            font_size=14,
            font_family="Source Sans",
        ),
    )

    return fig


def map_preview(institutions_df: pd.DataFrame) -> go.Figure:
    """Create a world map preview of university destinations."""

    fig = px.scatter_geo(
        institutions_df,
        lat="latitude",
        lon="longitude",
        size="student_count",
        projection="equirectangular",
    )

    fig.update_traces(
        marker=dict(
            color="#e2703e",
            line=dict(width=0),
        ),
        hoverinfo="skip",
        hovertemplate=None,
    )

    fig.update_geos(
        fitbounds="locations",
        showland=True,
        landcolor="#fafaf8",
        showcountries=True,
        showocean=True,
        oceancolor="#d4dadc",
        countrycolor="#f3eaea",
        showcoastlines=False,
        showframe=False,
        lataxis_showgrid=False,
        lonaxis_showgrid=False,
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=MAP_PREVIEW_HEIGHT,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig