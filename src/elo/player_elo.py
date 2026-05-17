"""
Squad Strength Score (SSS) and form adjustments on top of base ELO.
"""

import pandas as pd
from src.utils.constants import (
    POSITION_WEIGHTS, FORM_DECAY_WEIGHTS, FORM_WINDOW,
    STARTER_WEIGHT, BENCH_WEIGHT,
    AVG_SQUAD_STRENGTH, AVG_FORM_SCORE,
    SQUAD_ELO_SCALE, FORM_ELO_SCALE,
    STAR_PLAYERS,
)
from src.utils.helpers import weighted_mean, clamp


def player_strength_score(row: pd.Series) -> float:
    """
    Compute a single Player Strength Score (PSS 0-100) from FIFA attributes.
    Expects columns: overall, potential, composure, stamina, reactions.
    A 'form' column is used if present.
    """
    weights = {
        "overall":    0.40,
        "potential":  0.10,
        "composure":  0.10,
        "stamina":    0.08,
        "reactions":  0.07,
    }
    score = sum(row.get(col, 70) * w for col, w in weights.items())
    if "form" in row.index:
        score += row["form"] * 0.25
    else:
        score += 70 * 0.25  # neutral default
    return round(clamp(score, 0, 100), 2)


def squad_strength_score(
    team_name: str,
    fifa_df: pd.DataFrame,
    injured_players: list = None,
) -> float:
    """
    Weighted average PSS for the best available 11 + bench.
    """
    injured_players = injured_players or []
    squad = (
        fifa_df[
            (fifa_df["nationality"] == team_name)
            & (~fifa_df["short_name"].isin(injured_players))
        ]
        .sort_values("PSS", ascending=False)
    )

    if squad.empty:
        return AVG_SQUAD_STRENGTH

    starters = squad.head(11)["PSS"].values
    bench    = squad.iloc[11:18]["PSS"].values

    sss = starters.mean() * STARTER_WEIGHT
    if len(bench):
        sss += bench.mean() * BENCH_WEIGHT
    return round(sss, 2)


def recent_form_score(
    player_name: str,
    as_of_date,
    ratings_df: pd.DataFrame,
) -> float:
    """
    Weighted average of last FORM_WINDOW match ratings for one player.
    ratings_df must have: player_name, date, rating (0-10), goals, assists.
    """
    recent = (
        ratings_df[
            (ratings_df["player_name"] == player_name)
            & (ratings_df["date"] < pd.Timestamp(as_of_date))
        ]
        .sort_values("date", ascending=False)
        .head(FORM_WINDOW)
    )

    if recent.empty:
        return AVG_FORM_SCORE

    w = FORM_DECAY_WEIGHTS[: len(recent)]
    base = weighted_mean(recent["rating"].tolist(), w)
    goal_bonus   = recent["goals"].sum()   * 0.10
    assist_bonus = recent["assists"].sum() * 0.05
    return round(clamp(base + goal_bonus + assist_bonus, 0, 10), 2)


def team_form_score(
    lineup: list,          # [(player_name, position), ...]
    as_of_date,
    ratings_df: pd.DataFrame,
) -> float:
    """
    Position-weighted team form score.
    """
    if not lineup:
        return AVG_FORM_SCORE

    total, weight_sum = 0.0, 0.0
    for player, position in lineup:
        form = recent_form_score(player, as_of_date, ratings_df)
        w    = POSITION_WEIGHTS.get(position, 0.08)
        total      += form * w
        weight_sum += w
    return round(total / weight_sum if weight_sum else AVG_FORM_SCORE, 2)


def adjusted_elo(
    base_elo: float,
    squad_strength: float,
    team_form: float,
) -> float:
    """
    Adjust base ELO using squad quality and recent player form.
    """
    squad_delta = (squad_strength - AVG_SQUAD_STRENGTH) * SQUAD_ELO_SCALE
    form_delta  = (team_form      - AVG_FORM_SCORE)     * FORM_ELO_SCALE
    return round(base_elo + squad_delta + form_delta, 1)


def star_player_score(
    team: str,
    injured_list: list,
    fifa_df: pd.DataFrame,
) -> float:
    """
    Average PSS of available star players. Returns 0 if team not in STAR_PLAYERS.
    """
    stars = STAR_PLAYERS.get(team, [])
    if not stars:
        return AVG_SQUAD_STRENGTH

    available = [p for p in stars if p not in injured_list]
    scores = []
    for p in available:
        row = fifa_df[fifa_df["short_name"] == p]
        if not row.empty:
            scores.append(float(row.iloc[0]["PSS"]))
        else:
            scores.append(75.0)
    return round(sum(scores) / len(stars), 2)  # penalise missing stars
