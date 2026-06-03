# Implementation Plan: PyTorch MLP & Training Pipeline

## Project Hardening Rules

- Persist the scaler and model artifacts together so inference cannot drift from training.
- Keep the train/validation split reproducible and explicitly document the random seed.
- Compare every candidate model against the baseline before promoting it.
- Validate loss curves, artifact paths, and hyperparameter logs before the track is considered stable.
- Preserve the training input contract defined by the core pipeline track.

## Phase 1: Model Topology & Loss Function

- [ ] Task: Build neural network sequential MLP model class
  - [ ] Define PyTorch Sequential architecture with customizable layers, ReLU activations, and Dropout layers.
  - [ ] Write unit tests to check model initialization and forward pass shapes.
  - [ ] Implement MLP code in `training/model.py`.
- [ ] Task: Integrate Huber Loss function
  - [ ] Create test case validating that Huber Loss computes correctly.
  - [ ] Set Huber Loss as the optimization criterion.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Model Topology & Loss Function' (Protocol in workflow.md)

## Phase 2: Training & Validation Loop

- [ ] Task: Create data pipeline for model ingestion
  - [ ] Write tests for loading train/val partitions and scaling logic.
  - [ ] Implement data loaders and scaling preprocessing utility.
- [ ] Task: Build training loop logic
  - [ ] Write unit tests asserting single epoch forward/backward step.
  - [ ] Implement training and evaluation loops with log outputs.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Training & Validation Loop' (Protocol in workflow.md)

## Phase 3: Hyperparameter Tuning Grid

- [ ] Task: Build tuning orchestrator
  - [ ] Test the tuning controller with a small sub-grid.
  - [ ] Implement grid search logic over learning rate, dropout rate, and dense unit capacity.
  - [ ] Save the best weights (`.pth`) and preprocessing scaler.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Hyperparameter Tuning Grid' (Protocol in workflow.md)
