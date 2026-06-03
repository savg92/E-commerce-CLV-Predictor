import numpy as np
import pytest
from backend.domain.baseline import RandomForestBaseline, evaluate_predictions

def test_random_forest_baseline_fit_predict():
    # Simple linear/non-linear test data
    X_train = np.array([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0], [5.0, 6.0]])
    y_train = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    
    baseline = RandomForestBaseline(n_estimators=10, random_state=42)
    baseline.fit(X_train, y_train)
    
    predictions = baseline.predict(X_train)
    assert len(predictions) == 5
    # Random Forest regression should fit training data decently well
    # Check that predictions are close to actuals
    assert predictions[0] == pytest.approx(10.0, abs=5.0)

def test_evaluate_predictions():
    y_true = np.array([10.0, 20.0, 30.0])
    y_pred = np.array([11.0, 19.0, 30.5])
    
    metrics = evaluate_predictions(y_true, y_pred)
    assert "mae" in metrics
    assert "r2" in metrics
    assert "mse" in metrics
    
    assert metrics["mae"] == pytest.approx(0.833, abs=0.01)
    assert metrics["r2"] > 0.9

def test_run_training():
    import tempfile
    import os
    from backend.training.train_baseline import run_training
    
    # Generate mock transaction data for 10 customers over observation & target windows
    # Customer ID, Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Country
    lines = ["Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country"]
    
    # 10 customers
    # We want observation window (e.g. 2009-12-01 to 2010-08-30 (9 months))
    # and future window (e.g. 2010-09-01 onwards)
    for i in range(10):
        cust_id = f"1000{i}"
        # Obs purchase
        lines.append(f"100{i},85123A,Prod,5,2009-12-05 10:00:00,2.5,{cust_id},UK")
        lines.append(f"101{i},85123A,Prod,2,2010-01-05 11:00:00,2.5,{cust_id},UK")
        # Target purchase (future CLV)
        lines.append(f"102{i},85123A,Prod,10,2010-10-05 12:00:00,3.0,{cust_id},UK")
        
    csv_content = "\n".join(lines)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = f.name
        
    try:
        train_metrics, val_metrics = run_training(temp_path)
        assert "mae" in train_metrics
        assert "r2" in train_metrics
        assert "mae" in val_metrics
        assert "r2" in val_metrics
    finally:
        os.remove(temp_path)

