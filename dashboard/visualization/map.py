from textwrap import fill

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.config import REFERENCE_DATA


def world_map(institutions_df: pd.DataFrame) -> go.Figure:
    """Create an interactive map of university destinations."""

    institutions_df["wrapped_name"] = institutions_df["institution"].apply(
        lambda x: fill(x, width=28).replace("\n", "<br>")
    )

    hover_text = [
        (
            f"<b>🏛️ {row.wrapped_name}</b>"
            "<br>"
            f"{'' 
               if row.campus == REFERENCE_DATA.default_values["campus"] 
               else f'<br>📍 {row.campus}'}"
            f"<br>🌍 {row.country}"
            f"<br>👨‍🎓 {row.student_count} "
            f"{'student' if row.student_count == 1 else 'students'}"
        )
        for row in institutions_df.itertuples(index=False)
    ]

    df = institutions_df.assign(hover=hover_text)
    df = df.assign(marker_size= 2 + institutions_df["student_count"] ** 1.5 * 5)

    fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude",
        size="marker_size",
        custom_data=["hover"],
        height=500,
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