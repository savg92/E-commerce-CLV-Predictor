"""Reusable data preparation utilities for PyTorch training."""

from __future__ import annotations

import datetime
import os
import tempfile
from dataclasses import dataclass

import numpy as np
import pandas as pd

from backend.domain import entities, services, use_cases
from backend.infrastructure import data_loaders


FEATURE_COLUMNS = [
    "Country",
    "RecencyDays",
    "TenureDays",
    "Frequency",
    "Monetary",
    "AvgBasketValue",
    "AvgBasketQuantity",
    "UniqueProducts",
    "AverageUnitPrice",
]


@dataclass(frozen=True, slots=True)
class TrainingSplit:
    """Container holding the processed train/validation data bundle."""

    train_frame: pd.DataFrame
    val_frame: pd.DataFrame
    X_train: np.ndarray
    X_val: np.ndarray
    y_train: np.ndarray
    y_val: np.ndarray
    preprocessor: services.FeaturePreprocessor


def _load_transactions(data_path: str):
    """Load transactions from CSV or Excel into domain entities."""

    if data_path.endswith((".xlsx", ".xls")):
        df = pd.read_excel(data_path)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as temp_file:
            temp_path = temp_file.name
            df.to_csv(temp_path, index=False)
        try:
            return data_loaders.CSVTransactionRepository(temp_path).load_transactions()
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return data_loaders.CSVTransactionRepository(data_path).load_transactions()


def _build_customer_frame(
    transactions: list[entities.Transaction], train_ratio: float
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Convert transactions into chronological train and validation frames."""

    if not transactions:
        raise ValueError("No valid transactions found in data file.")

    dates = [transaction.invoice_date for transaction in transactions]
    cutoff_date = min(dates) + datetime.timedelta(days=9 * 30)

    customer_transactions: dict[str, list[entities.Transaction]] = {}
    for transaction in transactions:
        customer_transactions.setdefault(transaction.customer_id, []).append(transaction)

    splitter = services.TemporalSplitter()
    use_case = use_cases.CalculateRFM()

    rfm_records = []
    for customer_id, tx_list in customer_transactions.items():
        obs_transactions, future_transactions = splitter.split_transactions(tx_list, cutoff_date)
        if obs_transactions:
            rfm_records.append(
                use_case.execute(
                    customer_id=customer_id,
                    obs_transactions=obs_transactions,
                    future_transactions=future_transactions,
                    cutoff_date=cutoff_date,
                )
            )

    if not rfm_records:
        raise ValueError("No customer features calculated. Check observation window/cutoff date.")

    customer_frame = pd.DataFrame(rfm_records)
    train_frame, val_frame = splitter.split_train_val(customer_frame, train_ratio=train_ratio)
    return train_frame, val_frame


def build_training_split(data_path: str, train_ratio: float = 0.8) -> TrainingSplit:
    """Build the train/validation bundle used by the PyTorch trainer."""

    transactions = _load_transactions(data_path)
    train_frame, val_frame = _build_customer_frame(transactions, train_ratio=train_ratio)

    preprocessor = services.FeaturePreprocessor()
    X_train_raw = train_frame[FEATURE_COLUMNS]
    X_val_raw = val_frame[FEATURE_COLUMNS]
    y_train = train_frame["Future_CLV"].to_numpy(dtype=float)
    y_val = val_frame["Future_CLV"].to_numpy(dtype=float)

    X_train = preprocessor.fit_transform(X_train_raw)
    X_val = preprocessor.transform(X_val_raw)

    return TrainingSplit(
        train_frame=train_frame,
        val_frame=val_frame,
        X_train=X_train,
        X_val=X_val,
        y_train=y_train,
        y_val=y_val,
        preprocessor=preprocessor,
    )