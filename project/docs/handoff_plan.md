# Deployment Handoff Plan

- Clone the repository, create a Python environment, and install `requirements.txt` using the commands in `README.md`.
- Verify `data/raw/hs300_daily_metadata.json`, its SHA-256 checksum, date range, and row count before any scoring run.
- Run `notebooks/project_pipeline.ipynb` top to bottom and confirm the scenario table and API-test outputs are visible.
- Use `python -m src.run_step ...` for the independently schedulable cleaning task; review `logs/pipeline.log` on failure.
- Start `app.py` only after `model/regime_model.joblib` has passed the notebook and unit checks.
- Link the operations dashboard to the thresholds and owners in `docs/monitoring_plan.md`.
- Keep the most recent approved model artifact available for rollback; never approve an overwrite based only on in-sample fit.
- Log source, model, and business incidents in the repository issue tracker and assign the owner named in the monitoring plan.
- Escalate breached model or allocation thresholds to the risk chair; the API output must remain advisory until approval is restored.
