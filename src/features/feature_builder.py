"""
Merge ELO history + match features + player features into features_final.csv.
"""

import os
import pandas as pd
from tqdm import tqdm

from src.features.match_features import (
    h2h_stats, venue_form, recent_form_points,
    days_since_last_match, goals_avg,
)

PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def build_features() -> pd.DataFrame:
    matches_path   = os.path.join(PROCESSED, "matches_clean.csv")
    elo_path       = os.path.join(PROCESSED, "elo_history.csv")
    squad_path     = os.path.join(PROCESSED, "squad_strength.csv")

    for p in [matches_path, elo_path]:
        if not os.path.exists(p):
            raise FileNotFoundError(f"Missing {p} — run earlier pipeline steps first.")

    matches = pd.read_csv(matches_path, parse_dates=["date"])
    elo_hist = pd.read_csv(elo_path, parse_dates=["date"])

    # Merge ELO onto matches
    df = matches.merge(
        elo_hist[["date", "home_team", "away_team",
                  "home_elo_before", "away_elo_before"]],
        on=["date", "home_team", "away_team"],
        how="left",
    )
    df["elo_diff"] = df["home_elo_before"] - df["away_elo_before"]

    # Squad strength (static — uses latest FIFA data)
    if os.path.exists(squad_path):
        sq = pd.read_csv(squad_path).set_index("team")["squad_strength"]
        df["home_squad_strength"] = df["home_team"].map(sq).fillna(70.0)
        df["away_squad_strength"] = df["away_team"].map(sq).fillna(70.0)
        df["squad_strength_diff"] = df["home_squad_strength"] - df["away_squad_strength"]
    else:
        df["squad_strength_diff"] = 0.0

    rows = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Features"):
        h, a, d = row.home_team, row.away_team, row.date

        h2h   = h2h_stats(matches, h, a, d)
        vf    = venue_form(matches, h, str(row.get("city", "")), d)
        h_frm = recent_form_points(matches, h, d)
        a_frm = recent_form_points(matches, a, d)
        h_rest = days_since_last_match(matches, h, d)
        a_rest = days_since_last_match(matches, a, d)
        h_gs, h_gc = goals_avg(matches, h, d)
        a_gs, a_gc = goals_avg(matches, a, d)

        rows.append({
            "date":                row.date,
            "home_team":           h,
            "away_team":           a,
            "result":              row.result,
            "tournament_weight":   row.tournament_weight,
            "elo_diff":            row.get("elo_diff", 0),
            "home_elo":            row.get("home_elo_before", 1500),
            "away_elo":            row.get("away_elo_before", 1500),
            "squad_strength_diff": row.get("squad_strength_diff", 0),
            "home_recent_form":    h_frm,
            "away_recent_form":    a_frm,
            "h2h_home_wins":       h2h["h2h_home_wins"],
            "h2h_draws":           h2h["h2h_draws"],
            "h2h_away_wins":       h2h["h2h_away_wins"],
            "venue_win_rate":      vf,
            "home_goals_avg":      h_gs,
            "away_goals_avg":      a_gs,
            "home_goals_conceded": h_gc,
            "away_goals_conceded": a_gc,
            "days_rest_home":      h_rest,
            "days_rest_away":      a_rest,
            "is_neutral":          int(row.neutral),
        })

    features = pd.DataFrame(rows)
    out = os.path.join(PROCESSED, "features_final.csv")
    features.to_csv(out, index=False)
    print(f"  Saved feature table ({len(features):,} rows × {features.shape[1]} cols) → {out}")
    return features
