import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import numpy as np
from collections import defaultdict
from fastapi import APIRouter
from src.models.predict import predict_match

router = APIRouter()

TEAMS = [
    "Brazil", "France", "Argentina", "England", "Spain", "Germany",
    "Portugal", "Netherlands", "Belgium", "Italy", "Croatia", "Uruguay",
    "Mexico", "United States", "Morocco", "Senegal", "Japan", "South Korea",
    "Australia", "Ecuador", "Colombia", "Poland", "Switzerland", "Denmark",
    "Austria", "Turkey", "Serbia", "Ukraine", "Iran", "Saudi Arabia",
    "Canada", "Qatar",
]

@router.get("/simulate")
def simulate(n: int = 1000):
    wins = defaultdict(int)
    for _ in range(min(n, 5000)):
        pool = TEAMS.copy()
        np.random.shuffle(pool)
        while len(pool) > 1:
            nxt = []
            for j in range(0, len(pool) - 1, 2):
                h, a = pool[j], pool[j+1]
                try:
                    p = predict_match(h, a, is_neutral=True)
                    o = np.random.choice(
                        ["home_win", "draw", "away_win"],
                        p=[p["home_win"], p["draw"], p["away_win"]]
                    )
                    nxt.append(h if o in ("home_win", "draw") else a)
                except:
                    nxt.append(h)
            if len(pool) % 2 == 1:
                nxt.append(pool[-1])
            pool = nxt
        if pool:
            wins[pool[0]] += 1
    return sorted(
        [{"team": t, "probability": round(w / n * 100, 1)} for t, w in wins.items()],
        key=lambda x: -x["probability"]
    )