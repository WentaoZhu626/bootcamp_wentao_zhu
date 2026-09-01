"""Time-aware Hidden Markov Model training, scoring, and persistence."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler

from src.features import FEATURE_COLUMNS
from src.outliers import clip_to_training_bounds


# hmmlearn logs tiny negative final likelihood deltas as warnings even when a
# usable fitted model is returned. The pipeline treats fit failures as errors,
# while suppressing that numerical-noise message in stakeholder notebooks.
logging.getLogger("hmmlearn.base").setLevel(logging.ERROR)


@dataclass(frozen=True)
class ModelSpec:
    name: str = "baseline_5_state"
    n_states: int = 5
    holding_period: int = 20
    initial_train_periods: int = 80
    training_window_periods: int = 100
    refit_every: int = 5
    n_iter: int = 100
    random_state: int = 42
    clip_outliers: bool = True
    transaction_cost_bps: float = 5.0


def _fit_model(train: pd.DataFrame, spec: ModelSpec, feature_columns: list[str]) -> dict:
    scaler = StandardScaler().fit(train[feature_columns])
    transformed = scaler.transform(train[feature_columns])
    model = GaussianHMM(
        n_components=spec.n_states,
        covariance_type="diag",
        n_iter=spec.n_iter,
        tol=1e-3,
        min_covar=1e-4,
        random_state=spec.random_state,
    ).fit(transformed)
    states = model.predict(transformed)
    state_returns = (
        pd.DataFrame({"state": states, "future_return": train["future_return"].to_numpy()})
        .groupby("state")["future_return"]
        .mean()
        .reindex(range(spec.n_states))
        .fillna(train["future_return"].mean())
        .to_dict()
    )
    return {
        "model": model,
        "scaler": scaler,
        "state_returns": {int(k): float(v) for k, v in state_returns.items()},
        "feature_columns": feature_columns,
        "context_features": train[feature_columns].copy(),
    }


def walk_forward_hmm(
    observations: pd.DataFrame,
    spec: ModelSpec,
    feature_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Generate out-of-sample signals using only data available at each date."""
    features = feature_columns or FEATURE_COLUMNS
    if len(observations) <= spec.initial_train_periods:
        raise ValueError("not enough observations for the configured training period")

    rows = []
    artifact = None
    for index in range(spec.initial_train_periods, len(observations)):
        start = max(0, index - spec.training_window_periods)
        train = observations.iloc[start:index].copy()
        current = observations.iloc[[index]].copy()
        if spec.clip_outliers:
            train, current = clip_to_training_bounds(train, current, features)
        if artifact is None or (index - spec.initial_train_periods) % spec.refit_every == 0:
            artifact = _fit_model(train, spec, features)

        sequence = pd.concat([train[features], current[features]], ignore_index=True)
        transformed = artifact["scaler"].transform(sequence)
        current_state = int(artifact["model"].predict(transformed)[-1])
        predicted_return = float(artifact["state_returns"][current_state])
        position = int(predicted_return > 0)
        row = observations.iloc[index]
        rows.append(
            {
                "date": row["date"],
                "next_date": row["next_date"],
                "future_return": float(row["future_return"]),
                "predicted_return": predicted_return,
                "state": current_state,
                "position": position,
                "scenario": spec.name,
            }
        )

    result = pd.DataFrame(rows)
    result["turnover"] = result["position"].diff().abs().fillna(result["position"].abs())
    fee = spec.transaction_cost_bps / 10_000
    result["strategy_return"] = result["position"] * result["future_return"] - fee * result["turnover"]
    result["benchmark_return"] = result["future_return"]
    result["strategy_nav"] = (1 + result["strategy_return"]).cumprod()
    result["benchmark_nav"] = (1 + result["benchmark_return"]).cumprod()
    result["direction_correct"] = (
        np.sign(result["predicted_return"]) == np.sign(result["future_return"])
    )
    return result


def fit_final_artifact(
    observations: pd.DataFrame,
    spec: ModelSpec,
    output_path: str | Path,
    feature_columns: list[str] | None = None,
    latest_features: dict[str, float] | None = None,
    data_through: str | None = None,
) -> dict:
    """Fit the deployable model on the latest training window and save it."""
    features = feature_columns or FEATURE_COLUMNS
    train = observations.tail(spec.training_window_periods).copy()
    bounds = {column: tuple(train[column].quantile([0.01, 0.99])) for column in features}
    clipped = train.copy()
    for column, (low, high) in bounds.items():
        clipped[column] = clipped[column].clip(low, high)
    artifact = _fit_model(clipped, spec, features)
    artifact.update(
        {
            "spec": spec,
            "feature_bounds": bounds,
            "trained_through": data_through or str(train["next_date"].max().date()),
            "latest_features": latest_features or observations.iloc[-1][features].astype(float).to_dict(),
            "version": "1.0.0",
        }
    )
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, output)
    return artifact


def predict_features(artifact: dict, features: dict[str, float]) -> dict:
    """Validate one feature record and return a deployable regime decision."""
    names = artifact["feature_columns"]
    missing = set(names) - set(features)
    extra = set(features) - set(names)
    if missing or extra:
        raise ValueError(f"feature keys mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
    values = []
    for name in names:
        value = float(features[name])
        low, high = artifact["feature_bounds"][name]
        values.append(min(max(value, low), high))
    current = pd.DataFrame([values], columns=names)
    context = artifact.get("context_features", pd.DataFrame(columns=names))
    sequence = pd.concat([context[names], current], ignore_index=True)
    transformed = artifact["scaler"].transform(sequence)
    state = int(artifact["model"].predict(transformed)[-1])
    expected = float(artifact["state_returns"][state])
    return {
        "state": state,
        "regime": "risk_on" if expected > 0 else "risk_off",
        "recommended_exposure": 1 if expected > 0 else 0,
        "expected_period_return": expected,
        "model_version": artifact["version"],
        "trained_through": artifact["trained_through"],
    }
