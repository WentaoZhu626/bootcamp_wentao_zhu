# FRE 5040 Bootcamp Repository

This repository follows the course's required Git repository structure.
The recommended GitHub repository name is `bootcamp_wentao_zhu`.

## Repository areas

| Area | Purpose | Pushed to GitHub? |
| --- | --- | --- |
| `class_materials/` | Instructor handouts and lecture notebooks | No - ignored by Git |
| `homework/` | One self-contained folder per assigned stage | Yes |
| `project/` | The cumulative semester project | Yes |

`class_materials/` and `homework/` exist locally. Git does not track empty
folders, so `homework/homeworkNN/` should be created only when that assignment
starts. Do not add placeholder folders for future homework.

## Homework conventions

- Use one folder per stage, such as `homework/homework03/`.
- Keep the submission notebook at the homework folder root.
- Name it `homeworkNN_<stage-name>_submission.ipynb`.
- Add only the data, source, report, or model folders required by that stage.
- Copy instructor starter files out of `class_materials/`; never edit the clean
  originals there.

## Project conventions

The full project folder tree is created at setup time. Empty project folders
contain `.gitkeep` so that they appear on GitHub. Project paths are relative to
`project/`, use forward slashes, and never begin with `/` or `../`.

- `data/raw/`: direct, unedited inputs
- `data/processed/`: reproducible derived data
- `notebooks/`: project notebooks
- `src/`: reusable Python modules
- `reports/`: reader-facing deliverables
- `reports/images/`: saved figures
- `model/`: saved model objects
- `docs/`: internal design notes

Small course data files are committed. Real secrets belong in `.env`, which is
ignored; safe placeholders belong in `project/.env.example`, which is committed.
