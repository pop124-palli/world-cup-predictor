"""
Clean raw results.csv and write data/processed/matches_clean.csv.
"""

import os
import pandas as pd
from src.data.loader import load_results

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

# Normalise inconsistent country / team name spellings found in the Kaggle dataset
TEAM_NAME_MAP = {
    "USA":                      "United States",
    "IR Iran":                  "Iran",
    "Korea Republic":           "South Korea",
    "Korea DPR":                "North Korea",
    "Czech Republic":           "Czechia",
    "Cape Verde Islands":       "Cape Verde",
    "St. Kitts and Nevis":      "Saint Kitts and Nevis",
    "São Tomé and Príncipe":    "Sao Tome and Principe",
}


def _normalise_team_names(df: pd.DataFrame) -> pd.DataFrame:
    df["home_team"] = df["home_team"].replace(TEAM_NAME_MAP)
    df["away_team"] = df["away_team"].replace(TEAM_NAME_MAP)
    return df


def clean_data() -> pd.DataFrame:
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df = load_results()

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "home_team", "away_team", "home_score", "away_score"])

    # Fix team names
    df = _normalise_team_names(df)

    # Add result column: 0=home win, 1=draw, 2=away win
    df["result"] = (
        df.apply(
            lambda r: 0 if r.home_score > r.away_score
            else (1 if r.home_score == r.away_score else 2),
            axis=1,
        )
    )

    # Add a simple tournament weight
    def _tw(t):
        t = str(t).lower()
        if "world cup" in t and "qualif" not in t:
            return 3
        if "qualif" in t:
            return 2
        if "friendly" in t:
            return 1
        return 2

    df["tournament_weight"] = df["tournament"].apply(_tw)
    df = df.sort_values("date").reset_index(drop=True)

    out = os.path.join(PROCESSED_DIR, "matches_clean.csv")
    df.to_csv(out, index=False)
    print(f"  Saved {len(df):,} clean matches → {out}")
    return df
