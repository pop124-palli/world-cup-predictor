"""
Load saved model and print accuracy, confusion matrix, and SHAP summary.
"""

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False

PROCESSED = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
MODELS    = os.path.join(os.path.dirname(__file__), "..", "..", "models")

FEATURE_COLS = [
    "elo_diff", "squad_strength_diff",
    "home_recent_form", "away_recent_form",
    "h2h_home_wins", "h2h_draws", "h2h_away_wins",
    "venue_win_rate",
    "home_goals_avg", "away_goals_avg",
    "home_goals_conceded", "away_goals_conceded",
    "days_rest_home", "days_rest_away",
    "is_neutral", "tournament_weight",
]


def evaluate(model_name: str = "gbm_model.pkl") -> None:
    model  = joblib.load(os.path.join(MODELS, model_name))
    scaler = joblib.load(os.path.join(MODELS, "scaler.pkl"))

    df = pd.read_csv(os.path.join(PROCESSED, "features_final.csv")).dropna(subset=FEATURE_COLS)
    X = scaler.transform(df[FEATURE_COLS])
    y = df["result"].astype(int)

    preds = model.predict(X)
    print(f"Overall accuracy: {accuracy_score(y, preds):.4f}")

    cm = confusion_matrix(y, preds)
    disp = ConfusionMatrixDisplay(cm, display_labels=["Home Win", "Draw", "Away Win"])
    disp.plot(cmap="Blues")
    plt.title(f"Confusion Matrix — {model_name}")
    plt.tight_layout()
    plt.show()

    if HAS_SHAP:
        explainer = shap.Explainer(model, X)
        shap_vals = explainer(X[:500])
        shap.summary_plot(shap_vals, features=df[FEATURE_COLS].iloc[:500],
                          feature_names=FEATURE_COLS, plot_type="bar")


if __name__ == "__main__":
    evaluate()
