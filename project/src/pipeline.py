"""End-to-end project pipeline used by the cumulative notebook."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.cleaning import clean_market_data, cleaning_audit
from src.config import PROJECT_ROOT, Settings
from src.eda import eda_summary
from src.evaluation import bootstrap_mean_active_return, performance_metrics
from src.features import build_latest_features, build_period_observations
from src.ingest import acquire_hs300
from src.modeling import ModelSpec, fit_final_artifact, walk_forward_hmm
from src.outliers import iqr_outlier_flags
from src.reporting import create_eda_figures, create_evaluation_figures


def run_full_pipeline(refresh_data: bool = False, root: str | Path = PROJECT_ROOT) -> dict:
    """Run ingestion through reporting and return key in-memory artifacts."""
    project_root = Path(root)
    settings = Settings()
    raw_path = project_root / "data" / "raw" / "hs300_daily.csv"
    processed = project_root / "data" / "processed"
    images = project_root / "reports" / "images"
    model_path = project_root / "model" / "regime_model.joblib"
    processed.mkdir(parents=True, exist_ok=True)
    images.mkdir(parents=True, exist_ok=True)

    raw, metadata = acquire_hs300(
        raw_path,
        settings.start_date,
        settings.end_date,
        settings.symbol,
        settings.yfinance_symbol,
        refresh=refresh_data,
    )
    clean = clean_market_data(raw)
    clean["return_outlier"] = iqr_outlier_flags(clean["daily_return"], multiplier=3.0)
    audit = cleaning_audit(raw, clean)
    observations = build_period_observations(clean, settings.holding_period)

    clean.to_csv(processed / "hs300_clean.csv", index=False)
    clean.to_parquet(processed / "hs300_clean.parquet", index=False)
    observations.to_csv(processed / "period_features.csv", index=False)
    audit.to_csv(processed / "cleaning_audit.csv", index=False)
    eda = eda_summary(clean)
    eda.to_csv(processed / "eda_summary.csv", index=False)
    create_eda_figures(clean, observations, images)

    specs = [
        ModelSpec(name="baseline_5_state", n_states=5, clip_outliers=True),
        ModelSpec(name="3_state", n_states=3, clip_outliers=True),
        ModelSpec(name="4_state", n_states=4, clip_outliers=True),
        ModelSpec(name="no_feature_clipping", n_states=5, clip_outliers=False),
    ]
    backtests: dict[str, pd.DataFrame] = {}
    metric_rows = []
    for spec in specs:
        backtest = walk_forward_hmm(observations, spec)
        backtests[spec.name] = backtest
        metrics = performance_metrics(backtest, periods_per_year=252 / spec.holding_period)
        metrics["scenario"] = spec.name
        metric_rows.append(metrics)

    scenarios = pd.DataFrame(metric_rows)
    baseline = backtests["baseline_5_state"]
    uncertainty = bootstrap_mean_active_return(baseline)
    baseline.to_csv(processed / "walk_forward_predictions.csv", index=False)
    scenarios.to_csv(processed / "scenario_metrics.csv", index=False)
    (processed / "uncertainty_summary.json").write_text(json.dumps(uncertainty, indent=2))
    create_evaluation_figures(baseline, scenarios, images)

    baseline_spec = specs[0]
    latest_features = build_latest_features(clean, settings.holding_period)
    artifact = fit_final_artifact(
        observations,
        baseline_spec,
        model_path,
        latest_features=latest_features,
        data_through=str(clean["date"].max().date()),
    )
    return {
        "raw": raw,
        "metadata": metadata,
        "clean": clean,
        "audit": audit,
        "observations": observations,
        "eda": eda,
        "backtest": baseline,
        "scenarios": scenarios,
        "uncertainty": uncertainty,
        "artifact": artifact,
    }
