# Implementation Plan: PyTorch MLP & Training Pipeline

## Project Hardening Rules

- Persist the scaler and model artifacts together so inference cannot drift from training.
- Keep the train/validation split reproducible and explicitly document the random seed.
- Compare every candidate model against the baseline before promoting it.
- Validate loss curves, artifact paths, and hyperparameter logs before the track is considered stable.
- Preserve the training input contract defined by the core pipeline track.

## Phase 1: Model Topology & Loss Function [checkpoint: 36210cb]

- [x] Task: Build neural network sequential MLP model class
  - [x] Define PyTorch Sequential architecture with customizable layers, ReLU activations, and Dropout layers.
  - [x] Write unit tests to check model initialization and forward pass shapes.
  - [x] Implement MLP code in `training/model.py`.
        _Summary:_ Added `backend.training.MLP` as a sequential PyTorch regressor with configurable hidden layers, ReLU activations, dropout, and output width. Added tests that validate the forward-pass shape and layer composition.
- [x] Task: Integrate Huber Loss function
  - [x] Create test case validating that Huber Loss computes correctly.
  - [x] Set Huber Loss as the optimization criterion.
        _Summary:_ Added `build_huber_loss()` to return a configured `torch.nn.HuberLoss` and covered it with a deterministic unit test verifying the expected loss value for a simple residual example.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Model Topology & Loss Function' (Protocol in workflow.md)
  _Summary:_ Verified the phase by running the training-focused backend test suite and full project tests with coverage. Confirmed the new PyTorch module imports cleanly and the monorepo test command remains green.

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
