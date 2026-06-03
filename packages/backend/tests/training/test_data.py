import os
import tempfile

import numpy as np

from backend.training.data import build_training_split


def test_build_training_split_produces_chronological_train_val_and_scaled_features():
    lines = ["Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country"]

    for i in range(10):
        cust_id = f"1000{i}"
        lines.append(f"100{i},85123A,Prod,5,2009-12-05 10:00:00,2.5,{cust_id},UK")
        lines.append(f"101{i},85123A,Prod,2,2010-01-05 11:00:00,2.5,{cust_id},UK")
        lines.append(f"102{i},85123A,Prod,10,2010-10-05 12:00:00,3.0,{cust_id},UK")

    csv_content = "\n".join(lines)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    try:
        bundle = build_training_split(temp_path)

        assert len(bundle.train_frame) == 8
        assert len(bundle.val_frame) == 2
        assert bundle.X_train.shape[0] == 8
        assert bundle.X_val.shape[0] == 2
        assert bundle.X_train.shape[1] == bundle.X_val.shape[1]
        assert np.nanmin(bundle.X_train) >= 0.0
        assert np.nanmax(bundle.X_train) <= 1.0
        assert list(bundle.train_frame["CustomerID"]) == [f"1000{i}" for i in range(8)]
        assert list(bundle.val_frame["CustomerID"]) == [f"1000{i}" for i in range(8, 10)]
    finally:
        os.remove(temp_path)
