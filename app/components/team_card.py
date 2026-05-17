import streamlit as st
import pandas as pd
import os

PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def team_card(team_name: str) -> None:
    """Display a simple info card for a national team."""
    st.subheader(team_name)

    snap = os.path.join(PROCESSED, "elo_snapshot.csv")
    if os.path.exists(snap):
        df = pd.read_csv(snap)
        row = df[df["team"] == team_name]
        if not row.empty:
            st.metric("ELO Rating", f"{row.iloc[0]['elo']:.0f}")

    sq_path = os.path.join(PROCESSED, "squad_strength.csv")
    if os.path.exists(sq_path):
        df2 = pd.read_csv(sq_path)
        row2 = df2[df2["team"] == team_name]
        if not row2.empty:
            st.metric("Squad Strength", f"{row2.iloc[0]['squad_strength']:.1f}")
