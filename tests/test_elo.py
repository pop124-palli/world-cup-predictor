"""Unit tests for ELO calculation logic."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from collections import defaultdict
from src.elo.base_elo import expected_score, update_match_elo
from src.utils.constants import DEFAULT_ELO


def test_expected_score_equal_teams():
    assert abs(expected_score(1500, 1500) - 0.5) < 1e-9


def test_expected_score_stronger_team():
    assert expected_score(2000, 1500) > 0.5


def test_elo_increases_on_win():
    elo = defaultdict(lambda: DEFAULT_ELO)
    elo["A"] = 1500
    elo["B"] = 1500
    before = elo["A"]
    update_match_elo(elo, "A", "B", 1, 0, True, "Friendly")
    assert elo["A"] > before


def test_elo_decreases_on_loss():
    elo = defaultdict(lambda: DEFAULT_ELO)
    before = elo["A"]
    update_match_elo(elo, "A", "B", 0, 1, True, "Friendly")
    assert elo["A"] < before


def test_draw_on_equal_teams_no_change():
    elo = defaultdict(lambda: DEFAULT_ELO)
    elo["A"] = elo["B"] = 1500
    update_match_elo(elo, "A", "B", 1, 1, True, "Friendly")
    # Small change expected since expected score ~ 0.5 and actual = 0.5
    assert abs(elo["A"] - 1500) < 1.0


if __name__ == "__main__":
    test_expected_score_equal_teams()
    test_expected_score_stronger_team()
    test_elo_increases_on_win()
    test_elo_decreases_on_loss()
    test_draw_on_equal_teams_no_change()
    print("All ELO tests passed ✅")
