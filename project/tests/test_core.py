from pathlib import Path
import sys

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.cleaning import clean_market_data
from src.features import FEATURE_COLUMNS, build_period_observations
from src.modeling import predict_features


def test_cleaning_and_features():
    raw = pd.read_csv(ROOT / "data" / "raw" / "hs300_daily.csv")
    clean = clean_market_data(raw)
    observations = build_period_observations(clean, holding_period=20)
    assert clean["date"].is_monotonic_increasing
    assert not observations[FEATURE_COLUMNS].isna().any().any()


def test_saved_model_prediction_schema():
    artifact = joblib.load(ROOT / "model" / "regime_model.joblib")
    result = predict_features(artifact, artifact["latest_features"])
    assert result["regime"] in {"risk_on", "risk_off"}
    assert result["recommended_exposure"] in {0, 1}
