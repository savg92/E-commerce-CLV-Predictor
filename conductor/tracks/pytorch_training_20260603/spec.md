# Specification: PyTorch MLP & Training Pipeline

## Overview
Implement the deep learning core for predicting customer lifetime value (CLV) based on the historical RFM (Recency, Frequency, Monetary) transactional data.

## Functional Requirements
- **Neural Network Architecture:** Multi-Layer Perceptron (MLP) built in PyTorch with ReLU activation functions and Dropout for regularization.
- **Robust Loss Function:** Use Huber Loss to manage heavy right-skewed transactional outlier data (whales).
- **Training Pipeline:** Transition from notebooks to Python training script `training/train_final.py` which split dataset 80/20 train/validation.
- **Hyperparameter Grid Search:** Grid tuning for learning rates (0.001, 0.0001), dropout rates (0.2, 0.3), and dense unit counts (256, 1024).
- **Artifact Saving:** Export the best-trained PyTorch weights (`.pth`) and preprocessing scaler.

## Non-Functional Requirements
- Validation loss improvement over linear baseline models.
- Fully automated training execution via Makefile.

## Acceptance Criteria
- Running `make train` (or equivalent python command) successfully starts and finishes the MLP training pipeline.
- Outputs the trained model file and the corresponding data scaler file.
- Comprehensive log logs training and validation losses.
