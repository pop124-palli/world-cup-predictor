"""Unit tests for feature helper functions."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from src.features.match_features import h2h_stats, recent_form_points, goals_avg


def _sample_df():
    return pd.DataFrame({
        "date":       pd.to_datetime(["2020-01-01", "2020-06-01", "2021-01-01"]),
        "home_team":  ["Brazil", "Brazil", "France"],
        "away_team":  ["France", "Argentina", "Brazil"],
        "home_score": [2, 1, 0],
        "away_score": [1, 0, 2],
        "neutral":    [False, False, True],
        "result":     [0, 0, 2],
        "city":       ["Rio", "Sao Paulo", "Paris"],
        "tournament_weight": [3, 2, 3],
    })


def test_h2h_stats_returns_dict():
    df = _sample_df()
    result = h2h_stats(df, "Brazil", "France", "2022-01-01")
    assert isinstance(result, dict)
    assert "h2h_home_wins" in result


def test_recent_form_no_matches():
    df = _sample_df()
    # Germany has no matches — should return neutral default
    form = recent_form_points(df, "Germany", "2022-01-01")
    assert form == 1.0


def test_goals_avg_returns_tuple():
    df = _sample_df()
    scored, conceded = goals_avg(df, "Brazil", "2022-01-01")
    assert isinstance(scored, float)
    assert isinstance(conceded, float)


if __name__ == "__main__":
    test_h2h_stats_returns_dict()
    test_recent_form_no_matches()
    test_goals_avg_returns_tuple()
    print("All feature tests passed ✅")
