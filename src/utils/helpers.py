"""
Small reusable utility functions.
"""

import math
import pandas as pd


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Return a/b, or default if b is zero."""
    return a / b if b != 0 else default


def date_diff_days(d1, d2) -> int:
    """Return absolute difference in days between two date-like values."""
    return abs((pd.Timestamp(d1) - pd.Timestamp(d2)).days)


def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp value between lo and hi."""
    return max(lo, min(hi, value))


def weighted_mean(values, weights) -> float:
    """Weighted average. Lists must be the same length."""
    if not values:
        return 0.0
    total_w = sum(weights[:len(values)])
    return sum(v * w for v, w in zip(values, weights)) / total_w if total_w else 0.0


def get_k_factor(tournament: str, k_map: dict) -> float:
    """Look up K-factor for a tournament string."""
    for key, val in k_map.items():
        if key.lower() in tournament.lower():
            return val
    return k_map.get("default", 20)
