import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict
from src.models.predict import predict_match

st.title("🏆 2026 World Cup Simulator")

# 48-team field (representative subset for demo)
DEFAULT_TEAMS = [
    "Brazil", "France", "Argentina", "England", "Spain", "Germany",
    "Portugal", "Netherlands", "Belgium", "Italy", "Croatia", "Uruguay",
    "Mexico", "United States", "Morocco", "Senegal", "Japan", "South Korea",
    "Australia", "Ecuador", "Colombia", "Chile", "Poland", "Switzerland",
    "Denmark", "Austria", "Turkey", "Serbia", "Ukraine", "Iran",
    "Saudi Arabia", "Qatar",
]

n_sims = st.slider("Number of simulations", 100, 5000, 1000, step=100)

if st.button("Run Monte Carlo Simulation ▶", type="primary"):
    wins = defaultdict(int)
    teams = DEFAULT_TEAMS

    progress = st.progress(0)
    for i in range(n_sims):
        pool = teams.copy()
        np.random.shuffle(pool)
        # Simple single-elimination bracket
        while len(pool) > 1:
            next_round = []
            for j in range(0, len(pool) - 1, 2):
                h, a = pool[j], pool[j+1]
                try:
                    p = predict_match(h, a, is_neutral=True)
                    r = np.random.choice(["home_win", "draw", "away_win"],
                                         p=[p["home_win"], p["draw"], p["away_win"]])
                    next_round.append(h if r in ("home_win", "draw") else a)
                except Exception:
                    next_round.append(h)
            if len(pool) % 2 == 1:
                next_round.append(pool[-1])
            pool = next_round
        wins[pool[0]] += 1
        progress.progress((i + 1) / n_sims)

    progress.empty()
    results = (
        pd.DataFrame({"team": list(wins.keys()), "wins": list(wins.values())})
        .sort_values("wins", ascending=False)
        .assign(probability=lambda d: d.wins / n_sims)
    )

    import plotly.express as px
    fig = px.bar(results.head(16), x="probability", y="team", orientation="h",
                 title=f"Tournament Win Probability ({n_sims:,} simulations)",
                 color="probability", color_continuous_scale="Greens")
    fig.update_layout(yaxis=dict(autorange="reversed"), xaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(results, use_container_width=True)
