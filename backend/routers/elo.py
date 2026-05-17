import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter()
PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

@router.get("/elo/{team_name}")
def elo_history(team_name: str):
    p = os.path.join(PROCESSED, "elo_history.csv")
    if not os.path.exists(p):
        raise HTTPException(404, "ELO history not found. Run pipeline.py first.")
    df = pd.read_csv(p, parse_dates=["date"])
    home = df[df["home_team"] == team_name][["date", "home_elo_after"]].rename(
        columns={"home_elo_after": "elo"})
    away = df[df["away_team"] == team_name][["date", "away_elo_after"]].rename(
        columns={"away_elo_after": "elo"})
    hist = pd.concat([home, away]).sort_values("date")
    hist["date"] = hist["date"].dt.strftime("%Y-%m-%d")
    return hist.tail(200).to_dict(orient="records")