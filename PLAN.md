# Project Roadmap: E-commerce CLV Predictor

This document provides the milestone-level roadmap for the project. Each milestone below maps to a corresponding Conductor track for detailed execution, status, and checkpoint tracking. For the live registry, refer to the [Conductor Tracks Registry](./conductor/tracks.md).

## Project Goal

To model the complex, non-linear relationship between a customer's historical transactional behavior and their future monetary value (Customer Lifetime Value) using Deep Learning.

## Milestone 1: Core Foundation & Data Engineering

- [x] **Conductor Track:** [Scaffold Monorepo and Implement Core Data Pipeline](./conductor/tracks/core_pipeline_20260603/)
  - Scope: initialize `uv` and `bun` workspaces, implement the Clean Architecture data pipeline (Entities, Use Cases, Adapters), and establish the Random Forest baseline.
  - Exit criteria: reproducible workspace setup, validated RFM feature engineering, chronological data split, and a working baseline benchmark.

## Milestone 2: Deep Learning Implementation

- [~] **Conductor Track:** [Implement PyTorch MLP & Training Pipeline](./conductor/tracks/pytorch_training_20260603/)
  - Scope: define the MLP topology, implement the training loop with Huber Loss, and automate hyperparameter tuning.
  - Exit criteria: trainable model script, persisted weights and scaler artifacts, and repeatable validation metrics.

## Milestone 3: Inference Engine & Application Core

- [ ] **Conductor Track:** [Build FastAPI Inference API & React Dashboard](./conductor/tracks/inference_dashboard_20260603/)
  - Scope: load PyTorch weights in FastAPI, implement real-time inference with OOD safety alerts, and develop the React dashboard for visualization.
  - Exit criteria: `/predict` works against the live model, OOD warnings surface in the UI, and the end-to-end flow is verified.

## Milestone 4: DevOps & Deployment

- [ ] **Conductor Track:** [Dockerization & Cloud Deployment](./conductor/tracks/docker_deployment_20260603/)
  - Scope: containerize backend and frontend, configure CI/CD pipelines, and prepare deployment targets for cloud-native environments (Vercel/AWS).
  - Exit criteria: production-ready container builds, local multi-service orchestration, and documented deployment steps.

## Milestone 5: Documentation & Architecture

- [ ] **Conductor Track:** [Project Documentation and Architectural Blueprint](./conductor/tracks/documentation_blueprint_20260603/)
  - Scope: create comprehensive technical and functional documentation, generate Clean Architecture diagrams, document API endpoints and data schemas, and finalize the academic deliverables.
  - Exit criteria: complete README/user guides, architecture diagrams, API/model documentation, and submission-ready deliverables.

## Milestone Dependencies

1. Milestone 1 must be complete before any modeling or application work begins.
2. Milestone 2 depends on stable data pipeline artifacts from Milestone 1.
3. Milestone 3 depends on the persisted model and scaler outputs from Milestone 2.
4. Milestone 4 depends on a working inference application from Milestone 3.
5. Milestone 5 depends on the finalized implementation details produced by Milestones 1–4.

## Robustness Guardrails

- Reproducibility: use deterministic splits, fixed seeds where randomness is involved, and versioned artifacts for models and preprocessors.
- Data Integrity: validate schema, missing fields, outliers, and leakage before training or inference proceeds.
- Model Safety: never promote a model without baseline comparison, validation metrics, and OOD behavior documented.
- Delivery Safety: do not advance a milestone until tests, linting, and documentation checks are green for the associated track.
- Change Control: any scope, dependency, or contract change must be reflected in both this roadmap and the matching Conductor track plan.

## Delivery Rules

- Milestones should always mirror the current status in `conductor/tracks.md`.
- The active milestone here must match the active track in `conductor/tracks.md`.
- Only one track should be active at a time unless the track plan explicitly documents an overlap.
- Any change in scope, order, or dependency must be reflected in both this roadmap and the affected Conductor track.
