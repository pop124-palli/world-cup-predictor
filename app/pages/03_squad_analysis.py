import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🧑‍🤝‍🧑 Squad Strength Analysis")

PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
sq_path  = os.path.join(PROCESSED, "squad_strength.csv")
pss_path = os.path.join(PROCESSED, "player_pss.csv")

if not os.path.exists(sq_path):
    st.warning("Squad strength data not found. Run pipeline.py first.")
    st.stop()

sq  = pd.read_csv(sq_path)
top = sq.head(30)

fig = px.bar(top, x="squad_strength", y="team", orientation="h",
             title="Top 30 National Teams — Squad Strength Score",
             color="squad_strength", color_continuous_scale="Blues")
fig.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig, use_container_width=True)

if os.path.exists(pss_path):
    pss = pd.read_csv(pss_path)
    team = st.selectbox("Drill into a team", sorted(pss["nationality"].dropna().unique()))
    sub  = pss[pss["nationality"] == team].sort_values("PSS", ascending=False).head(23)
    st.dataframe(sub[["short_name", "club_name", "PSS"]], use_container_width=True)
