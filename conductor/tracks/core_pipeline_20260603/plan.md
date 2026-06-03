# Implementation Plan: Scaffold Monorepo and Implement Core Data Pipeline

## Phase 1: Environment & Monorepo Scaffold
This phase establishes the foundational structure for the monorepo, ensuring all tools are correctly configured.

- [ ] Task: Initialize `uv` workspace and root `pyproject.toml`
    - [ ] Create `pyproject.toml` with `uv` workspace configuration
    - [ ] Add base dependencies (Pandas, Scikit-Learn, PyTorch)
- [ ] Task: Initialize `bun` workspace and root `package.json`
    - [ ] Create `package.json` for the monorepo
    - [ ] Configure `bun` workspaces for frontend and backend components
- [ ] Task: Create root `Makefile` for orchestration
    - [ ] Define `setup`, `test`, and `lint` targets
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Environment & Monorepo Scaffold' (Protocol in workflow.md)

## Phase 2: Core Data Engineering Pipeline
This phase implements the logic to transform raw transactional data into high-quality features for modeling.

- [ ] Task: Implement RFM feature extraction logic
    - [ ] Write tests for Recency, Frequency, and Monetary calculation
    - [ ] Implement extraction logic following Clean Architecture principles
- [ ] Task: Implement Log-Transformation and Scaling utilities
    - [ ] Write tests for `np.log1p` and Min-Max scaling consistency
    - [ ] Implement reusable scaling pipeline
- [ ] Task: Implement Temporal Data Partitioning
    - [ ] Write tests for chronological split (Observation vs. Target windows)
    - [ ] Implement split logic to prevent data leakage
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Data Engineering Pipeline' (Protocol in workflow.md)

## Phase 3: Baseline Modeling & Validation
This phase establishes a performance baseline using a traditional non-linear model.

- [ ] Task: Implement RandomForest baseline regressor
    - [ ] Write tests for model training and prediction consistency
    - [ ] Implement training script with validation metrics (MAE, R²)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Baseline Modeling & Validation' (Protocol in workflow.md)
