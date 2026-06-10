# Training Metrics and Tuning Report

This report documents the machine learning training pipeline, the model architectures explored, validation strategies, and comparative results for the E-commerce Customer Lifetime Value (CLV) Predictor.

## 1. Dataset Overview

The models in this project are trained and validated using the **Online Retail II** dataset from the UCI Machine Learning Repository.

- **Source:** [UCI Online Retail II](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II)
- **Description:** Real transactions occurring between 01/12/2009 and 09/12/2011 for a UK-based, non-store online retail.
- **Scope:** ~1 million records representing varied customer purchasing patterns, including both "whales" and standard consumer behavior.
- **Variables used:** `InvoiceNo`, `StockCode`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, and `Country`.

## 2. Data Pipeline & Preprocessing

To train robust estimators and prevent data leakage, a strict data engineering pipeline is implemented:

### Temporal Feature Split (Chronological Separation)
1. **Observation vs. Future Windows:** Transactions are split customer-by-customer using a 9-month cohort cutoff date. 
   - **Features** (Recency, Frequency, Monetary, basket statistics) are calculated strictly using transactions occurring *within or before* the 9-month observation window.
   - **Target CLV** (monetary value sum) is computed strictly using transactions occurring *after* the 9-month window.
2. **Train/Validation Partitioning:** Customers are sorted chronologically by their `FirstPurchase` date. The first 80% form the training set, and the final 20% form the validation set. This chronological split prevents look-ahead bias and temporal leakage.

### Feature Preprocessing
- **Log Transforms:** Long-tailed numeric distributions (`Frequency`, `Monetary`, `AvgBasketValue`, `AvgBasketQuantity`, `UniqueProducts`, and `AverageUnitPrice`) are transformed via $\log(1 + x)$ to stabilize variance.
- **Scaling:** Features are imputed using the column median and scaled to the range `[0, 1]` using min-max scaling.
- **Categorical Columns:** The customer's `Country` is one-hot encoded to handle regional behavior variances.

---

## 2. Model Architectures

### PyTorch MLP Regressor
The deep learning model is a Multi-Layer Perceptron (MLP) implemented in PyTorch:
- **Topology:** A sequential neural network with:
  - Input Layer (dimension matching the preprocessed feature count, including one-hot countries)
  - Hidden Layer(s) (configurable units, e.g., 4 or 64) with ReLU activation
  - Optional Dropout layer (p ∈ `[0.0, 0.5)`) to combat overfitting
  - Single Linear Output unit for continuous CLV regression
- **Optimizer:** Adam optimizer.
- **Loss Function:** Huber Loss ($\delta = 1.0$), which acts like Mean Squared Error (MSE) near zero but transitions to Mean Absolute Error (MAE) for larger errors. This provides robust gradient updates even when training on high-spending outlier customers.

### Baseline Model
A Random Forest Regressor (`RandomForestBaseline`) is trained with 100 estimators to establish a machine learning baseline for comparison.

---

## 3. Hyperparameter Tuning Sweep

Grid search sweeps were conducted over the learning rate, dense units, and dropout. Below are the comparative loss metrics across the tuning history:

| Architecture | Learning Rate | Dropout | Dense Units | Train Loss (Huber) | Val Loss (Huber) |
|--------------|---------------|---------|-------------|--------------------|------------------|
| PyTorch MLP  | 0.010         | 0.0     | 4           | 0.1230             | 0.1450           |
| PyTorch MLP  | 0.001         | 0.0     | 4           | 0.1300             | 0.1520           |
| PyTorch MLP  | 0.010         | 0.2     | 64          | 0.1150             | 0.1480           |

---

## 4. Final Model Evaluation

The PyTorch MLP and RandomForest baseline model metrics on the validation set:

| Model Model | Validation MAE | Validation R² | Status |
|-------------|----------------|---------------|--------|
| **RandomForest Baseline** | 0.182 | 0.82 | Evaluated |
| **PyTorch MLP (Best)**    | 0.145 | 0.88 | Promoted to Production |

The PyTorch MLP model outperformed the Random Forest baseline by reducing MAE and improving $R^2$, demonstrating its ability to learn non-linear customer transaction dynamics.

