"""
Smoke test for prediction pipeline.
Skipped automatically if models have not been trained yet.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

MODELS = os.path.join(os.path.dirname(__file__), "..", "models")


def models_exist():
    return os.path.exists(os.path.join(MODELS, "scaler.pkl")) and any(
        os.path.exists(os.path.join(MODELS, f))
        for f in ("gbm_model.pkl", "xgb_model.pkl")
    )


@pytest.mark.skipif(not models_exist(), reason="Models not trained yet")
def test_predict_returns_three_probs():
    from src.models.predict import predict_match
    result = predict_match("Brazil", "France", is_neutral=True)
    assert "home_win" in result and "draw" in result and "away_win" in result
    total = result["home_win"] + result["draw"] + result["away_win"]
    assert abs(total - 1.0) < 0.01


if __name__ == "__main__":
    if models_exist():
        test_predict_returns_three_probs()
        print("Prediction test passed ✅")
    else:
        print("Skipped — run pipeline.py first to train models.")
