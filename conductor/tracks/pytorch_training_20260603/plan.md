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

## Phase 2: Training & Validation Loop [checkpoint: 8b50fd4]

- [x] Task: Create data pipeline for model ingestion
  - [x] Write tests for loading train/val partitions and scaling logic.
  - [x] Implement data loaders and scaling preprocessing utility.
        _Summary:_ Added `backend.training.build_training_split()` and `TrainingSplit` to reuse the core pipeline’s transaction loading, RFM engineering, chronological split, and scaling contract for PyTorch training.
- [x] Task: Build training loop logic
  - [x] Write unit tests asserting single epoch forward/backward step.
  - [x] Implement training and evaluation loops with log outputs.
        _Summary:_ Added `train_one_epoch()` and `evaluate()` helpers that move batches to the correct device, compute batchwise Huber loss, update model weights, and report averaged epoch metrics.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Training & Validation Loop' (Protocol in workflow.md)
      _Summary:_ Verified the phase by running the training-specific test set and the full monorepo test target, both of which passed cleanly with the new data bundle and epoch loop in place.

## Phase 3: Hyperparameter Tuning Grid [checkpoint: ce37b0b]

- [x] Task: Build tuning orchestrator
  - [x] Test the tuning controller with a small sub-grid.
  - [x] Implement grid search logic over learning rate, dropout rate, and dense unit capacity.
  - [x] Save the best weights (`.pth`) and preprocessing scaler.
        _Summary:_ Added `backend.training.run_hyperparameter_search()` with deterministic candidate evaluation, epoch-by-epoch training/evaluation, and persistence of the best model checkpoint plus fitted scaler to disk.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Hyperparameter Tuning Grid' (Protocol in workflow.md)
      _Summary:_ Verified the tuning grid by running the targeted tuning test and the full backend/monorepo test suite. Confirmed the best-artifact outputs are written and the training package remains stable.

## Phase: Review Fixes
- [x] Task: Apply review suggestions ee7d557
