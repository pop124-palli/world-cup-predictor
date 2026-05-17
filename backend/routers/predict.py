import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.predict import predict_match

router = APIRouter()

class MatchRequest(BaseModel):
    home: str
    away: str
    is_neutral: bool = False
    tournament_weight: int = 3

@router.post("/predict")
def predict(req: MatchRequest):
    try:
        r = predict_match(req.home, req.away, req.is_neutral, req.tournament_weight)
        return {
            "home": req.home,
            "away": req.away,
            "home_win": round(r["home_win"] * 100, 1),
            "draw":     round(r["draw"]     * 100, 1),
            "away_win": round(r["away_win"] * 100, 1),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))