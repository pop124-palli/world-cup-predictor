"""
Loop through every match in matches_clean.csv and build elo_history.csv.
"""

import os
from collections import defaultdict

import pandas as pd
from tqdm import tqdm

from src.utils.constants import DEFAULT_ELO
from src.elo.base_elo import update_match_elo

PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def run_elo() -> pd.DataFrame:
    matches_path = os.path.join(PROCESSED, "matches_clean.csv")
    if not os.path.exists(matches_path):
        raise FileNotFoundError("Run clean_data() first.")

    df = pd.read_csv(matches_path, parse_dates=["date"])
    elo: dict = defaultdict(lambda: DEFAULT_ELO)

    records = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="ELO"):
        home, away = row.home_team, row.away_team

        # Record ELO before the match
        records.append({
            "date":       row.date,
            "home_team":  home,
            "away_team":  away,
            "home_elo_before": round(elo[home], 1),
            "away_elo_before": round(elo[away], 1),
        })

        update_match_elo(
            elo, home, away,
            int(row.home_score), int(row.away_score),
            bool(row.neutral), str(row.tournament),
        )

        # Store post-match ELO too
        records[-1]["home_elo_after"] = round(elo[home], 1)
        records[-1]["away_elo_after"] = round(elo[away], 1)

    history = pd.DataFrame(records)
    out = os.path.join(PROCESSED, "elo_history.csv")
    history.to_csv(out, index=False)
    print(f"  Saved ELO history ({len(history):,} rows) → {out}")

    # Also save current ELO snapshot for every team
    snapshot = pd.DataFrame(
        [{"team": t, "elo": round(v, 1)} for t, v in elo.items()]
    ).sort_values("elo", ascending=False).reset_index(drop=True)
    snap_out = os.path.join(PROCESSED, "elo_snapshot.csv")
    snapshot.to_csv(snap_out, index=False)
    print(f"  Saved ELO snapshot ({len(snapshot)} teams) → {snap_out}")

    return history
