import argparse
import datetime
import os
import pandas as pd
import numpy as np
from typing import Tuple

from backend.infrastructure.data_loaders import CSVTransactionRepository
from backend.domain.use_cases import CalculateRFM
from backend.domain.services import FeaturePreprocessor, TemporalSplitter
from backend.domain.baseline import RandomForestBaseline, evaluate_predictions

def run_training(data_path: str) -> Tuple[dict, dict]:
    print(f"Loading data from {data_path}...")
    if data_path.endswith(".xlsx") or data_path.endswith(".xls"):
        # For excel files, we can save them temporarily as CSV or let pandas read them
        df = pd.read_excel(data_path)
        # Save as temporary CSV so we can reuse CSVTransactionRepository
        csv_path = data_path + ".temp.csv"
        df.to_csv(csv_path, index=False)
        repo = CSVTransactionRepository(csv_path)
    else:
        repo = CSVTransactionRepository(data_path)
        csv_path = None

    try:
        transactions = repo.load_transactions()
    finally:
        if csv_path and os.path.exists(csv_path):
            os.remove(csv_path)

    if not transactions:
        raise ValueError("No valid transactions found in data file.")

    print(f"Loaded {len(transactions)} valid transactions.")

    # Find global start date to compute 9-month cutoff
    dates = [t.invoice_date for t in transactions]
    min_date = min(dates)
    cutoff_date = min_date + datetime.timedelta(days=9 * 30) # approx 9 months
    print(f"Date range: {min_date} to {max(dates)}")
    print(f"Observation Cutoff Date: {cutoff_date}")

    # Group transactions by CustomerID
    customer_txs = {}
    for t in transactions:
        if t.customer_id not in customer_txs:
            customer_txs[t.customer_id] = []
        customer_txs[t.customer_id].append(t)

    # Split transactions per customer and calculate RFM
    splitter = TemporalSplitter()
    use_case = CalculateRFM()
    
    rfm_records = []
    for customer_id, tx_list in customer_txs.items():
        obs_tx, future_tx = splitter.split_transactions(tx_list, cutoff_date)
        # We only compute features if the customer had transactions in the observation window
        if obs_tx:
            rfm = use_case.execute(customer_id, obs_tx, future_tx, cutoff_date)
            rfm_records.append(rfm)

    if not rfm_records:
        raise ValueError("No customer features calculated. Check observation window/cutoff date.")

    customer_df = pd.DataFrame(rfm_records)
    print(f"Calculated RFM features for {len(customer_df)} customers.")

    # Chronological Split (80% Train / 20% Val)
    train_df, val_df = splitter.split_train_val(customer_df, train_ratio=0.8)
    print(f"Splits: Train={len(train_df)} customers, Validation={len(val_df)} customers.")

    # Define features and target
    feature_cols = [
        "Country", "RecencyDays", "TenureDays", 
        "Frequency", "Monetary", "AvgBasketValue", 
        "AvgBasketQuantity", "UniqueProducts", "AverageUnitPrice"
    ]
    
    X_train_raw = train_df[feature_cols]
    y_train = train_df["Future_CLV"].values
    
    X_val_raw = val_df[feature_cols]
    y_val = val_df["Future_CLV"].values

    # Preprocessing & Scaling
    preprocessor = FeaturePreprocessor()
    X_train = preprocessor.fit_transform(X_train_raw)
    X_val = preprocessor.transform(X_val_raw)

    print(f"Features shape post-processing: Train={X_train.shape}, Val={X_val.shape}")

    # Train RandomForest Baseline
    print("Training RandomForest baseline model...")
    baseline = RandomForestBaseline(n_estimators=100, random_state=42)
    baseline.fit(X_train, y_train)

    # Evaluate
    train_preds = baseline.predict(X_train)
    val_preds = baseline.predict(X_val)

    train_metrics = evaluate_predictions(y_train, train_preds)
    val_metrics = evaluate_predictions(y_val, val_preds)

    print("\n--- Training Results ---")
    print(f"Train MAE: {train_metrics['mae']:.4f}")
    print(f"Train R2:  {train_metrics['r2']:.4f}")
    print("\n--- Validation Results ---")
    print(f"Validation MAE: {val_metrics['mae']:.4f}")
    print(f"Validation R2:  {val_metrics['r2']:.4f}")

    return train_metrics, val_metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train RandomForest baseline model for E-commerce CLV Predictor.")
    parser.add_argument("--data-path", type=str, required=True, help="Path to transactional dataset (CSV or Excel).")
    args = parser.parse_args()
    
    run_training(args.data_path)
