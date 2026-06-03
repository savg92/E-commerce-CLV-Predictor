# Project Roadmap: E-commerce CLV Predictor

This document provides a high-level overview of the project's development milestones and active tracks. For detailed task tracking, refer to the [Conductor Tracks Registry](./conductor/tracks.md).

## Project Goal
To model the complex, non-linear relationship between a customer's historical transactional behavior and their future monetary value (Customer Lifetime Value) using Deep Learning.

## Milestone 1: Core Foundation & Data Engineering
- [ ] **Track: Scaffold Monorepo and Implement Core Data Pipeline**
  - Initialize `uv` and `bun` workspaces.
  - Implement Clean Architecture data pipeline (Entities, Use Cases, Adapters).
  - Establish baseline modeling with Random Forest.

## Milestone 2: Deep Learning Implementation
- [ ] **Track: Implement PyTorch MLP & Training Pipeline**
  - Define Neural Network topology.
  - Implement training loops with Huber Loss.
  - Automate hyperparameter tuning.

## Milestone 3: Inference Engine & Application Core
- [ ] **Track: Build FastAPI Inference API & React Dashboard**
  - Load PyTorch weights in FastAPI.
  - Implement real-time inference with OOD safety alerts.
  - Develop React dashboard for visualization.

## Milestone 4: DevOps & Deployment
- [ ] **Track: Dockerization & Cloud Deployment**
  - Containerize Backend and Frontend.
  - Configure CI/CD pipelines.
  - Deploy to cloud-native environments (Vercel/AWS).

## Milestone 5: Documentation & Architecture
- [ ] **Track: Project Documentation and Architectural Blueprint**
  - Create comprehensive technical and functional documentation.
  - Generate detailed architectural diagrams (Clean Architecture layers).
  - Document API endpoints, data schemas, and ML model performance.
  - Finalize README, user guides, and academic deliverables.
