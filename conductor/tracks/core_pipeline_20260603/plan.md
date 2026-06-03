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
This phase implements the logic to transform raw transactional data into high-quality features for modeling, adhering to Clean Architecture principles.

- [ ] Task: Define Domain Entities and Use Cases
    - [ ] Define `Customer` and `Transaction` entities in the Domain layer
    - [ ] Implement `CalculateRFM` use case with comprehensive business logic tests
- [ ] Task: Implement Data Adapters (Infrastructure Layer)
    - [ ] Create repository interfaces for data loading
    - [ ] Implement CSV and DB data loaders as concrete infrastructure adapters
- [ ] Task: Implement Log-Transformation and Scaling Services
    - [ ] Implement scaling logic as pure Domain services with unit tests
    - [ ] Implement reusable scaling pipeline for production inference
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

## Phase: Review Fixes
- [x] Task: Apply review suggestions a87f839
