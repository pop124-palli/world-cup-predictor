import plotly.graph_objects as go


def prob_chart(home: str, away: str, probs: dict) -> go.Figure:
    """Return a horizontal bar chart of win/draw/loss probabilities."""
    labels = [f"{home} Win", "Draw", f"{away} Win"]
    values = [probs.get("home_win", 0), probs.get("draw", 0), probs.get("away_win", 0)]
    colors = ["#2196F3", "#9E9E9E", "#FF5722"]

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=colors,
        text=[f"{v*100:.1f}%" for v in values],
        textposition="auto",
    ))
    fig.update_layout(
        title="Match Outcome Probabilities",
        xaxis=dict(tickformat=".0%", range=[0, 1]),
        height=250,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig
