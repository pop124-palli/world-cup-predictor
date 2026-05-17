import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pandas as pd
from fastapi import APIRouter

router = APIRouter()
PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

def _snap():
    p = os.path.join(PROCESSED, "elo_snapshot.csv")
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame(columns=["team", "elo"])

@router.get("/teams")
def get_teams():
    df = _snap().sort_values("elo", ascending=False)
    return [{"team": r.team, "elo": round(r.elo, 1)} for _, r in df.iterrows()]

@router.get("/teams/top")
def top_teams(n: int = 20):
    df = _snap().sort_values("elo", ascending=False).head(n)
    return [{"rank": i+1, "team": r.team, "elo": round(r.elo, 1)}
            for i, (_, r) in enumerate(df.iterrows())]

@router.get("/teams/{team_name}/squad")
def squad(team_name: str):
    p = os.path.join(PROCESSED, "player_pss.csv")
    if not os.path.exists(p): return []
    df = pd.read_csv(p)
    sub = df[df["nationality"] == team_name].sort_values("PSS", ascending=False).head(23)
    return sub[["short_name", "club_name", "PSS"]].fillna("").to_dict(orient="records")