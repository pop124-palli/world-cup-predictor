import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
from src.models.predict import predict_match

st.title("🔮 Match Predictor")

PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

@st.cache_data
def team_list():
    snap = os.path.join(PROCESSED, "elo_snapshot.csv")
    if os.path.exists(snap):
        return sorted(pd.read_csv(snap)["team"].tolist())
    return ["Brazil", "France", "Argentina", "England", "Spain",
            "Germany", "Portugal", "Netherlands"]

teams = team_list()

col1, col2 = st.columns(2)
with col1:
    home = st.selectbox("🏠 Home Team", teams, index=0)
with col2:
    away = st.selectbox("✈️ Away Team", teams, index=1)

neutral = st.checkbox("Neutral venue?")

if st.button("Predict Match", type="primary"):
    try:
        result = predict_match(home, away, is_neutral=neutral)
        st.subheader("Predicted Probabilities")
        c1, c2, c3 = st.columns(3)
        c1.metric(f"🏠 {home} Win", f"{result['home_win']*100:.1f}%")
        c2.metric("🤝 Draw",        f"{result['draw']*100:.1f}%")
        c3.metric(f"✈️ {away} Win", f"{result['away_win']*100:.1f}%")

        import plotly.graph_objects as go
        fig = go.Figure(go.Bar(
            x=[f"{home} Win", "Draw", f"{away} Win"],
            y=[result["home_win"], result["draw"], result["away_win"]],
            marker_color=["#1f77b4", "#aec7e8", "#ff7f0e"],
        ))
        fig.update_layout(yaxis_tickformat=".0%", title="Win Probability")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not predict: {e}. Make sure you've run pipeline.py first.")
