"""
Train GradientBoosting and XGBoost classifiers on features_final.csv.
Saves models/gbm_model.pkl and models/xgb_model.pkl.
"""

import os
import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

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


def train_model() -> None:
    os.makedirs(MODELS, exist_ok=True)
    path = os.path.join(PROCESSED, "features_final.csv")
    if not os.path.exists(path):
        raise FileNotFoundError("Run build_features() first.")

    df = pd.read_csv(path).dropna(subset=FEATURE_COLS + ["result"])
    X = df[FEATURE_COLS]
    y = df["result"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # GBM
    gbm = GradientBoostingClassifier(
        n_estimators=300, learning_rate=0.05,
        max_depth=4, subsample=0.8, random_state=42,
    )
    gbm.fit(X_train_s, y_train)
    gbm_acc = accuracy_score(y_test, gbm.predict(X_test_s))
    print(f"  GBM accuracy : {gbm_acc:.4f}")
    print(classification_report(y_test, gbm.predict(X_test_s),
                                 target_names=["Home Win", "Draw", "Away Win"]))

    joblib.dump(gbm,    os.path.join(MODELS, "gbm_model.pkl"))
    joblib.dump(scaler, os.path.join(MODELS, "scaler.pkl"))
    print(f"  Saved gbm_model.pkl and scaler.pkl → {MODELS}/")

    # XGBoost (optional)
    if HAS_XGB:
        xgb = XGBClassifier(
            n_estimators=300, learning_rate=0.05,
            max_depth=4, subsample=0.8,
            use_label_encoder=False, eval_metric="mlogloss",
            random_state=42, n_jobs=-1,
        )
        xgb.fit(X_train_s, y_train)
        xgb_acc = accuracy_score(y_test, xgb.predict(X_test_s))
        print(f"  XGB accuracy : {xgb_acc:.4f}")
        joblib.dump(xgb, os.path.join(MODELS, "xgb_model.pkl"))
        print(f"  Saved xgb_model.pkl → {MODELS}/")
    else:
        print("  (xgboost not installed — skipping XGB training)")
