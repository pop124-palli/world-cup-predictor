"""
Streamlit entry point.  Run with:
    streamlit run app/app.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(
    page_title="⚽ World Cup 2026 Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚽ World Cup 2026 Predictor")
st.markdown(
    """
    Welcome! Use the sidebar to navigate between pages:

    | Page | Description |
    |------|-------------|
    | 🔮 Match Predictor | Pick two teams and get win/draw/loss probabilities |
    | 📈 ELO Tracker | View any team's ELO rating over time |
    | 🧑‍🤝‍🧑 Squad Analysis | Compare squad strength between teams |
    | 🏆 Tournament Simulator | Simulate the full 2026 bracket |
    """
)
