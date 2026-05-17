"""
Functions to load raw CSVs from data/raw/.
"""

import os
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")


def _path(filename: str) -> str:
    return os.path.join(RAW_DIR, filename)


def load_results() -> pd.DataFrame:
    return pd.read_csv(_path("results.csv"))


def load_goalscorers() -> pd.DataFrame:
    return pd.read_csv(_path("goalscorers.csv"))


def load_shootouts() -> pd.DataFrame:
    return pd.read_csv(_path("shootouts.csv"))


def load_fifa_players() -> pd.DataFrame:
    return pd.read_csv(_path("fifa_players.csv"))


def load_rankings() -> pd.DataFrame:
    return pd.read_csv(_path("rankings.csv"))


def load_player_ratings() -> pd.DataFrame:
    return pd.read_csv(_path("player_ratings.csv"))
