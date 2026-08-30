# Course Project

This directory contains the cumulative FRE 5040 course project.

## Layout

- `data/raw/` stores source data exactly as acquired.
- `data/processed/` stores outputs that project code can reproduce.
- `notebooks/` stores the project's notebooks. The cumulative notebook should
  be named `project_pipeline.ipynb` when it is introduced by the course.
- `src/` stores reusable functions extracted from notebooks.
- `reports/` stores summaries and other reader-facing deliverables.
- `reports/images/` stores generated figures.
- `model/` stores serialized models.
- `docs/` stores design notes, assumptions, and plans.

Run project notebooks from this directory's context so imports such as
`from src...` and paths such as `data/raw/...` resolve consistently. Never put
files directly inside `data/`; use `data/raw/` or `data/processed/`.
