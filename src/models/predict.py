"""
Load trained model and return win/draw/loss probabilities for any two teams.
"""

import os
import joblib
import numpy as np
import pandas as pd

MODELS    = os.path.join(os.path.dirname(__file__), "..", "..", "models")
PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

FEATURE_COLS = [
    "elo_diff", "squad_strength_diff",
    "home_recent_form", "away_recent_form",
    "h2h_home_wins", "h2h_draws", "h2h_away_wins",
    "venue_win_rate",
    "home_goals_avg", "away_goals_avg",
    "home_goals_conceded", "away_goals_conceded",
    "days_rest_home", "days_rest_away",
    "is_neutral", "tournament_weight",
]

_model  = None
_scaler = None


def _load():
    global _model, _scaler
    if _model is None:
        for name in ("xgb_model.pkl", "gbm_model.pkl"):
            p = os.path.join(MODELS, name)
            if os.path.exists(p):
                _model = joblib.load(p)
                break
        _scaler = joblib.load(os.path.join(MODELS, "scaler.pkl"))


def _get_elo(team: str) -> float:
    snap = os.path.join(PROCESSED, "elo_snapshot.csv")
    if not os.path.exists(snap):
        return 1500.0
    df = pd.read_csv(snap)
    row = df[df["team"] == team]
    return float(row.iloc[0]["elo"]) if not row.empty else 1500.0


def _get_squad_strength(team: str) -> float:
    path = os.path.join(PROCESSED, "squad_strength.csv")
    if not os.path.exists(path):
        return 70.0
    df = pd.read_csv(path)
    row = df[df["team"] == team]
    return float(row.iloc[0]["squad_strength"]) if not row.empty else 70.0


def predict_match(
    home: str,
    away: str,
    is_neutral: bool = False,
    tournament_weight: int = 3,
) -> dict:
    """
    Return {"home_win": p, "draw": p, "away_win": p} for a given fixture.
    """
    _load()

    h_elo = _get_elo(home)
    a_elo = _get_elo(away)
    h_sq  = _get_squad_strength(home)
    a_sq  = _get_squad_strength(away)

    features = {
        "elo_diff":            h_elo - a_elo,
        "squad_strength_diff": h_sq  - a_sq,
        "home_recent_form":    1.5,   # neutral default
        "away_recent_form":    1.5,
        "h2h_home_wins":       0,
        "h2h_draws":           0,
        "h2h_away_wins":       0,
        "venue_win_rate":      0.5,
        "home_goals_avg":      1.2,
        "away_goals_avg":      1.2,
        "home_goals_conceded": 1.0,
        "away_goals_conceded": 1.0,
        "days_rest_home":      7,
        "days_rest_away":      7,
        "is_neutral":          int(is_neutral),
        "tournament_weight":   tournament_weight,
    }

    X = np.array([[features[c] for c in FEATURE_COLS]])
    X_s = _scaler.transform(X)
    probs = _model.predict_proba(X_s)[0]

    # Map class indices to labels (sorted: 0=home, 1=draw, 2=away)
    classes = _model.classes_
    label_map = {0: "home_win", 1: "draw", 2: "away_win"}
    result = {label_map[c]: round(float(p), 4) for c, p in zip(classes, probs)}
    return result
