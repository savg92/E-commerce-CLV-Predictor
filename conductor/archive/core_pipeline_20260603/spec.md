# Track Specification: Scaffold Monorepo and Implement Core Data Pipeline

## Goal
Establish a production-ready monorepo structure and implement the core data engineering pipeline required for CLV prediction. This foundation follows Clean Architecture principles and supports both Python (uv) and JavaScript/TypeScript (Bun).

## Scope
- **Monorepo Scaffolding:** Root configuration for `uv` (Python) and `bun` (JS/TS).
- **Orchestration:** Root `Makefile` for task automation.
- **Data Pipeline (Python):** RFM feature engineering, data cleaning, and scaling.
- **Baseline Modeling:** Implementation of a Random Forest regressor to serve as a performance benchmark.

## Technical Requirements
- **Environment:** `uv` for Python dependency management, `bun` for JS/TS.
- **Architecture:** Monorepo structure with clear separation between data science logic and application code.
- **Data Engineering:**
  - Handle missing `CustomerID`s and outliers.
  - Temporal feature splitting (Observation vs. Target windows).
  - Log-transformation and Min-Max scaling.
- **Baseline:** `RandomForestRegressor` from Scikit-Learn.

## Acceptance Criteria
- Monorepo successfully initialized with `uv sync` and `bun install`.
- Data pipeline transforms raw transaction logs into scaled RFM features.
- Baseline model achieves a non-trivial R² score on validation data.
- All code passes linting and achieves >85% test coverage.
