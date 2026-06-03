# Agent Instructions

This repository uses `PLAN.md` and the `conductor/` folder as the source of truth for project progress.

## Required workflow

- Before starting work, review `PLAN.md` and the relevant Conductor track plan.
- Keep the roadmap and active track status aligned.
- For each completed milestone or finished track phase, update the corresponding plan file and commit those changes.
- When a track is finished, mark it complete in the relevant Conductor plan and ensure the top-level roadmap reflects the same status.
- Prefer small, incremental changes with tests or documentation updates when applicable.

## Tooling conventions

- Use `make` for project orchestration and task entrypoints whenever a repo command exists.
- Use `uv` for Python dependency management, environments, and Python-side execution.
- Use `bun` for JavaScript/TypeScript dependency management and frontend execution.
- Keep commands consistent with the toolchain already established in `Makefile`, `pyproject.toml`, and `package.json`.
- Do not mix package managers or bypass the defined orchestration unless a task explicitly requires it.

## Commit discipline

- Update the plan before the implementation commit.
- Commit the plan update separately when the workflow calls for it.
- Do not leave milestone or track status changes unrecorded.

## Project guardrails

- Preserve the exact OOD warning text required by the product docs.
- Keep data pipeline, model, and inference contracts synchronized.
- Treat chronological splitting and leakage prevention as mandatory.
- Prefer reproducible, documented commands and deterministic outputs wherever possible.
