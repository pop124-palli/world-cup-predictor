"""
Compute per-match features: H2H stats, venue form, days rest, etc.
"""

import pandas as pd
import numpy as np
from src.utils.helpers import safe_divide, date_diff_days


def h2h_stats(df: pd.DataFrame, home: str, away: str, before_date) -> dict:
    """
    Last-5 head-to-head record between home and away before a given date.
    """
    mask = (
        (
            ((df.home_team == home) & (df.away_team == away))
            | ((df.home_team == away) & (df.away_team == home))
        )
        & (df.date < pd.Timestamp(before_date))
    )
    h2h = df[mask].sort_values("date", ascending=False).head(5)

    home_wins, draws, away_wins = 0, 0, 0
    for _, r in h2h.iterrows():
        if r.home_team == home:
            if r.home_score > r.away_score:
                home_wins += 1
            elif r.home_score == r.away_score:
                draws += 1
            else:
                away_wins += 1
        else:
            if r.away_score > r.home_score:
                home_wins += 1
            elif r.home_score == r.away_score:
                draws += 1
            else:
                away_wins += 1

    return {"h2h_home_wins": home_wins, "h2h_draws": draws, "h2h_away_wins": away_wins}


def venue_form(df: pd.DataFrame, team: str, city: str, before_date) -> float:
    """
    Team's win rate at a specific city in past matches.
    """
    mask = (
        ((df.home_team == team) | (df.away_team == team))
        & (df.city == city)
        & (df.date < pd.Timestamp(before_date))
    )
    past = df[mask].tail(10)
    if past.empty:
        return 0.5

    wins = 0
    for _, r in past.iterrows():
        if r.home_team == team and r.home_score > r.away_score:
            wins += 1
        elif r.away_team == team and r.away_score > r.home_score:
            wins += 1
    return round(safe_divide(wins, len(past)), 3)


def recent_form_points(
    df: pd.DataFrame, team: str, before_date, last_n: int = 5
) -> float:
    """
    Points from last N matches (W=3, D=1, L=0).  Returns average points per match.
    """
    mask = (
        ((df.home_team == team) | (df.away_team == team))
        & (df.date < pd.Timestamp(before_date))
    )
    recent = df[mask].sort_values("date", ascending=False).head(last_n)
    if recent.empty:
        return 1.0  # neutral default

    pts = 0
    for _, r in recent.iterrows():
        if r.home_team == team:
            pts += 3 if r.home_score > r.away_score else (1 if r.home_score == r.away_score else 0)
        else:
            pts += 3 if r.away_score > r.home_score else (1 if r.home_score == r.away_score else 0)
    return round(safe_divide(pts, len(recent)), 3)


def days_since_last_match(df: pd.DataFrame, team: str, before_date) -> int:
    """
    Number of days since team's previous match before the given date.
    """
    mask = (
        ((df.home_team == team) | (df.away_team == team))
        & (df.date < pd.Timestamp(before_date))
    )
    past = df[mask].sort_values("date", ascending=False)
    if past.empty:
        return 30  # default
    return date_diff_days(before_date, past.iloc[0].date)


def goals_avg(df: pd.DataFrame, team: str, before_date, last_n: int = 10) -> tuple:
    """
    Returns (avg_goals_scored, avg_goals_conceded) over last N matches.
    """
    mask = (
        ((df.home_team == team) | (df.away_team == team))
        & (df.date < pd.Timestamp(before_date))
    )
    recent = df[mask].sort_values("date", ascending=False).head(last_n)
    if recent.empty:
        return 1.2, 1.2

    scored, conceded = [], []
    for _, r in recent.iterrows():
        if r.home_team == team:
            scored.append(r.home_score)
            conceded.append(r.away_score)
        else:
            scored.append(r.away_score)
            conceded.append(r.home_score)

    return round(np.mean(scored), 3), round(np.mean(conceded), 3)
