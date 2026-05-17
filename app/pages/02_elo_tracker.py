import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 ELO Tracker")

PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
elo_path = os.path.join(PROCESSED, "elo_history.csv")

if not os.path.exists(elo_path):
    st.warning("ELO history not found. Run pipeline.py first.")
    st.stop()

@st.cache_data
def load_elo():
    df = pd.read_csv(elo_path, parse_dates=["date"])
    home = df[["date", "home_team", "home_elo_after"]].rename(
        columns={"home_team": "team", "home_elo_after": "elo"})
    away = df[["date", "away_team", "away_elo_after"]].rename(
        columns={"away_team": "team", "away_elo_after": "elo"})
    return pd.concat([home, away]).sort_values("date")

history = load_elo()
all_teams = sorted(history["team"].unique())
selected  = st.multiselect("Select teams", all_teams, default=all_teams[:5])

if selected:
    sub = history[history["team"].isin(selected)]
    fig = px.line(sub, x="date", y="elo", color="team", title="ELO Rating Over Time")
    st.plotly_chart(fig, use_container_width=True)
