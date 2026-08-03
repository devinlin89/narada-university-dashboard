import plotly.graph_objects as go

TICK_FONT = dict(
    family="Source sans, sans-serif",
    size=14,
)

AXIS_FONT = dict(
    family="Source sans, sans-serif",
    size=16,
)

BODY_FONT = dict(
    family="Source sans, sans-serif",
    size=14,
)

def style_figure(fig: go.Figure):
    fig.update_layout(
        autosize=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(automargin=True),
    )

    fig.update_xaxes(
        title_font=AXIS_FONT,
        tickfont=TICK_FONT,
    )

    fig.update_yaxes(
        title_font=AXIS_FONT,
        tickfont=TICK_FONT,
    )

    fig.update_traces(
        hoverinfo="skip",
        hovertemplate=None,
    )

    return fig