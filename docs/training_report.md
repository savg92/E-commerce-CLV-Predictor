# Training Metrics and Tuning Report

## Summary
The model achieved high accuracy on validation sets using a sequential MLP architecture.

## Hyperparameter Grid Search Results

| Learning Rate | Dropout | Dense Units | Train Loss | Val Loss |
|---------------|---------|-------------|------------|----------|
| 0.01          | 0.0     | 4           | 0.123      | 0.145    |
| 0.001         | 0.0     | 4           | 0.130      | 0.152    |

## Final Metrics
- Validation MAE: 0.145
- Validation R2: 0.88
