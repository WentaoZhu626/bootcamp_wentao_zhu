# FRE 5040 Bootcamp Repository

This repository contains the course homework submissions and a complete Stage 01-16 project lifecycle.

## Featured Project

### CSI 300 Hidden-State Risk Allocation

The project studies whether a Gaussian Hidden Markov Model can identify recurring CSI 300 market regimes and support a transparent 20-trading-day full-index/cash exposure review. It includes traceable raw data, reusable source modules, executed notebooks, chronological walk-forward evaluation, scenario and uncertainty analysis, a stakeholder report, a saved model and Flask API, monitoring and handoff plans, orchestration documentation, and a full lifecycle guide.

- [Project overview and run instructions](project/README.md)
- [Stakeholder report](project/reports/final_report.md)
- [Final lifecycle guide](project/docs/lifecycle_framework_guide.md)

The current conclusion is risk-aware: historical results are encouraging, but assumption sensitivity and an active-return confidence interval containing zero support shadow monitoring rather than immediate deployment.

## Repository Areas

| Area | Purpose | Pushed to GitHub? |
|---|---|---|
| `class_materials/` | Instructor handouts and lecture notebooks | No - ignored by Git |
| `homework/` | One self-contained folder per assigned stage | Yes |
| `project/` | Cumulative Stage 01-16 project | Yes |

## Conventions

- Each homework lives in `homework/homeworkNN/`.
- Instructor originals stay in ignored `class_materials/`.
- The cumulative project uses `data/raw/`, `data/processed/`, `notebooks/`, `src/`, `docs/`, `reports/`, and `model/`.
- Real secrets belong in ignored `.env` files; safe placeholders belong in tracked `.env.example` files.
- Small course datasets and reproducible outputs are committed so grading does not depend on live network access.
