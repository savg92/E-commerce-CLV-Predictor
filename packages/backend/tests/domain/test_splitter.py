import datetime
import pandas as pd
import pytest
from backend.domain.entities import Transaction
from backend.domain.services import TemporalSplitter

def test_temporal_splitter_transactions_split():
    # Setup some transactions
    t1 = Transaction("1", "A", "Desc", 1, datetime.datetime(2009, 12, 1), 1.0, "C1", "UK")
    t2 = Transaction("2", "B", "Desc", 1, datetime.datetime(2009, 12, 5), 1.0, "C1", "UK")
    t3 = Transaction("3", "C", "Desc", 1, datetime.datetime(2009, 12, 10), 1.0, "C1", "UK")
    
    cutoff_date = datetime.datetime(2009, 12, 6)
    
    obs, future = TemporalSplitter.split_transactions([t1, t2, t3], cutoff_date)
    
    assert len(obs) == 2
    assert t1 in obs
    assert t2 in obs
    assert len(future) == 1
    assert t3 in future

def test_temporal_splitter_train_val_split():
    # Setup customer data sorted by first purchase
    data = pd.DataFrame({
        "CustomerID": [f"C{i}" for i in range(10)],
        "FirstPurchase": [datetime.datetime(2009, 12, i) for i in range(1, 11)],
        "Future_CLV": [10.0 * i for i in range(1, 11)]
    })
    
    # 80/20 chronological split based on FirstPurchase
    train, val = TemporalSplitter.split_train_val(data, train_ratio=0.8)
    
    assert len(train) == 8
    assert len(val) == 2
    # Ensure they are sorted by FirstPurchase and split chronologically
    assert list(train["CustomerID"]) == [f"C{i}" for i in range(8)]
    assert list(val["CustomerID"]) == ["C8", "C9"]
