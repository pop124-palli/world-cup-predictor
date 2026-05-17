"""
Core ELO formula and K-factor logic.
"""

from src.utils.constants import HOME_ELO_BONUS, DEFAULT_ELO
from src.utils.helpers import get_k_factor
from src.utils.constants import K_FACTORS


def expected_score(elo_a: float, elo_b: float) -> float:
    """Probability that team A beats team B."""
    return 1.0 / (1.0 + 10.0 ** ((elo_b - elo_a) / 400.0))


def new_elo(old_elo: float, k: float, actual: float, expected: float) -> float:
    """Single ELO update step."""
    return old_elo + k * (actual - expected)


def update_match_elo(
    elo: dict,
    home: str,
    away: str,
    home_score: int,
    away_score: int,
    is_neutral: bool,
    tournament: str,
) -> None:
    """
    Update elo[home] and elo[away] in-place after one match.
    elo is a defaultdict(lambda: DEFAULT_ELO).
    """
    k = get_k_factor(tournament, K_FACTORS)
    bonus = 0 if is_neutral else HOME_ELO_BONUS

    exp_home = expected_score(elo[home] + bonus, elo[away])

    if home_score > away_score:
        actual = 1.0
    elif home_score == away_score:
        actual = 0.5
    else:
        actual = 0.0

    elo[home] = new_elo(elo[home], k, actual, exp_home)
    elo[away] = new_elo(elo[away], k, 1.0 - actual, 1.0 - exp_home)
