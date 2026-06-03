# Implementation Plan: Scaffold Monorepo and Implement Core Data Pipeline

## Project Hardening Rules

- Keep the dataset schema, feature definitions, and preprocessing artifacts versioned together.
- Treat chronological splits as a non-negotiable safeguard against leakage.
- Require deterministic behavior wherever randomness is introduced so pipeline runs are reproducible.
- Preserve the exact RFM feature contract for downstream training and inference tracks.
- Do not advance the track until the baseline benchmark, tests, and documentation agree on the same data contract.

## Phase 1: Environment & Monorepo Scaffold [checkpoint: dd44f4c]

This phase establishes the foundational structure for the monorepo, ensuring all tools are correctly configured.

- [x] Task: Initialize `uv` workspace and root `pyproject.toml`
  - [x] Create `pyproject.toml` with `uv` workspace configuration
  - [x] Add base dependencies (Pandas, Scikit-Learn, PyTorch)
        _Summary:_ Created root `pyproject.toml` with `uv` workspace referencing `packages/*` and added dependencies including pandas, scikit-learn, and torch. Created `packages/backend/pyproject.toml` as workspace member.
- [x] Task: Initialize `bun` workspace and root `package.json`
  - [x] Create `package.json` for the monorepo
  - [x] Configure `bun` workspaces for frontend and backend components
        _Summary:_ Created root `package.json` and `packages/frontend/package.json` configuring Bun workspaces.
- [x] Task: Create root `Makefile` for orchestration
  - [x] Define `setup`, `test`, and `lint` targets
        _Summary:_ Created root `Makefile` with targets for `setup`, `test`, and `lint` across frontend and backend.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Environment & Monorepo Scaffold' (Protocol in workflow.md)

## Phase 2: Core Data Engineering Pipeline [checkpoint: a984d16]

This phase implements the logic to transform raw transactional data into high-quality features for modeling, adhering to Clean Architecture principles.

- [x] Task: Define Domain Entities and Use Cases
  - [x] Define `Customer` and `Transaction` entities in the Domain layer
  - [x] Implement `CalculateRFM` use case with comprehensive business logic tests
        _Summary:_ Implemented Transaction and Customer domain entities with properties like line_amount. Implemented CalculateRFM use case and tested with 93% coverage.
- [x] Task: Implement Data Adapters (Infrastructure Layer)
  - [x] Create repository interfaces for data loading
  - [x] Implement CSV and DB data loaders as concrete infrastructure adapters
        _Summary:_ Created TransactionRepository abstraction in Domain. Implemented concrete CSVTransactionRepository to load and clean raw transactions using pandas, handling data-type standardizations, missing values, and filtering cancelations. Added DBTransactionRepository placeholder.
- [x] Task: Implement Log-Transformation and Scaling Services
  - [x] Implement scaling logic as pure Domain services with unit tests
  - [x] Implement reusable scaling pipeline for production inference
        _Summary:_ Implemented FeaturePreprocessor domain service, which wraps Scikit-Learn pipelines to impute features and apply MinMaxScaler and OneHotEncoder. Includes log-transformations for skewed columns and supports single customer dict input transformation.
- [x] Task: Implement Temporal Data Partitioning
  - [x] Write tests for chronological split (Observation vs. Target windows)
  - [x] Implement split logic to prevent data leakage
        _Summary:_ Implemented TemporalSplitter to split transaction logs into observation and future windows around a cutoff date, and chronologically split customers 80/20 train/validation.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Core Data Engineering Pipeline' (Protocol in workflow.md)

## Phase 3: Baseline Modeling & Validation

This phase establishes a performance baseline using a traditional non-linear model.

- [x] Task: Implement RandomForest baseline regressor
  - [x] Write tests for model training and prediction consistency
  - [x] Implement training script with validation metrics (MAE, R²)
        _Summary:_ Implemented RandomForestBaseline wrapper and metrics evaluation helper (`evaluate_predictions`). Implemented `train_baseline.py` to orchestrate end-to-end data loading, RFM calculation, scaling, splitting, and baseline model training. Added unit and integration tests.
- [~] Task: Conductor - User Manual Verification 'Phase 3: Baseline Modeling & Validation' (Protocol in workflow.md)

## Phase: Review Fixes

- [x] Task: Apply review suggestions a87f839
