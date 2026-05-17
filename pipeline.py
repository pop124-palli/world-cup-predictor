"""
pipeline.py  —  Master script. Run once to rebuild everything.
    python pipeline.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.data.cleaner import clean_data
from src.elo.elo_runner import run_elo
from src.features.feature_builder import build_features
from src.models.train import train_model


def main():
    print("\n=== Step 1 / 4 : Cleaning raw data ===")
    clean_data()

    print("\n=== Step 2 / 4 : Computing ELO ratings ===")
    run_elo()

    print("\n=== Step 3 / 4 : Building feature table ===")
    build_features()

    print("\n=== Step 4 / 4 : Training models ===")
    train_model()

    print("\n✅  Pipeline complete!")
    print("   Launch the app with:  streamlit run app/app.py")


if __name__ == "__main__":
    main()
