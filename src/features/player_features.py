"""
Compute PSS, SSS, and star-player availability features.
"""

import os
import pandas as pd
from src.data.loader import load_fifa_players
from src.elo.player_elo import (
    player_strength_score,
    squad_strength_score,
    star_player_score,
)

PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def build_pss_table() -> pd.DataFrame:
    """
    Compute PSS for every player in the FIFA dataset and save to
    data/processed/player_pss.csv.
    """
    os.makedirs(PROCESSED, exist_ok=True)
    fifa = load_fifa_players()

    # Ensure expected columns exist (fill with 70 if missing)
    for col in ["overall", "potential", "composure", "stamina", "reactions"]:
        if col not in fifa.columns:
            fifa[col] = 70

    fifa["PSS"] = fifa.apply(player_strength_score, axis=1)
    out = os.path.join(PROCESSED, "player_pss.csv")
    fifa[["short_name", "nationality", "club_name", "PSS"]].to_csv(out, index=False)
    print(f"  Saved PSS for {len(fifa):,} players → {out}")
    return fifa


def build_squad_strength_table(fifa_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute SSS for every national team and save to
    data/processed/squad_strength.csv.
    """
    os.makedirs(PROCESSED, exist_ok=True)
    teams = fifa_df["nationality"].dropna().unique()
    rows = []
    for team in teams:
        sss = squad_strength_score(team, fifa_df)
        rows.append({"team": team, "squad_strength": sss})
    df = pd.DataFrame(rows).sort_values("squad_strength", ascending=False)
    out = os.path.join(PROCESSED, "squad_strength.csv")
    df.to_csv(out, index=False)
    print(f"  Saved squad strength for {len(df)} teams → {out}")
    return df
