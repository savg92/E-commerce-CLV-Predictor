import pandas as pd
import pytest
from backend.domain.services import FeaturePreprocessor

def test_feature_preprocessor_fit_transform():
    # Mock data to fit the preprocessor
    data = pd.DataFrame([
        {"Country": "UK", "RecencyDays": 10, "TenureDays": 100, "Frequency": 5, "Monetary": 100.0, "AvgBasketValue": 20.0, "AvgBasketQuantity": 5.0, "UniqueProducts": 10, "AverageUnitPrice": 2.0},
        {"Country": "UK", "RecencyDays": 20, "TenureDays": 200, "Frequency": 10, "Monetary": 200.0, "AvgBasketValue": 20.0, "AvgBasketQuantity": 5.0, "UniqueProducts": 20, "AverageUnitPrice": 2.0},
        {"Country": "France", "RecencyDays": 30, "TenureDays": 300, "Frequency": 15, "Monetary": 300.0, "AvgBasketValue": 20.0, "AvgBasketQuantity": 5.0, "UniqueProducts": 30, "AverageUnitPrice": 2.0},
    ])
    
    preprocessor = FeaturePreprocessor()
    
    # Fit and transform
    X_trans = preprocessor.fit_transform(data)
    
    # Verify shape: 3 rows, and correct number of features
    # Numerical features (8) + one-hot encoded country features
    assert X_trans.shape[0] == 3
    # Check that it supports transform on new data
    new_data = pd.DataFrame([
        {"Country": "UK", "RecencyDays": 15, "TenureDays": 150, "Frequency": 7, "Monetary": 150.0, "AvgBasketValue": 21.0, "AvgBasketQuantity": 4.5, "UniqueProducts": 12, "AverageUnitPrice": 2.1}
    ])
    X_trans_new = preprocessor.transform(new_data)
    assert X_trans_new.shape[0] == 1
    assert X_trans_new.shape[1] == X_trans.shape[1]

def test_feature_preprocessor_single_inference():
    preprocessor = FeaturePreprocessor()
    # Fit with some data first
    data = pd.DataFrame([
        {"Country": "UK", "RecencyDays": 10, "TenureDays": 100, "Frequency": 5, "Monetary": 100.0, "AvgBasketValue": 20.0, "AvgBasketQuantity": 5.0, "UniqueProducts": 10, "AverageUnitPrice": 2.0},
        {"Country": "France", "RecencyDays": 30, "TenureDays": 300, "Frequency": 15, "Monetary": 300.0, "AvgBasketValue": 20.0, "AvgBasketQuantity": 5.0, "UniqueProducts": 30, "AverageUnitPrice": 2.0},
    ])
    preprocessor.fit(data)
    
    single_input = {
        "Country": "UK",
        "RecencyDays": 10,
        "TenureDays": 100,
        "Frequency": 5,
        "Monetary": 100.0,
        "AvgBasketValue": 20.0,
        "AvgBasketQuantity": 5.0,
        "UniqueProducts": 10,
        "AverageUnitPrice": 2.0
    }
    
    # Test single item transform (for FastAPI production inference)
    transformed = preprocessor.transform_single(single_input)
    assert len(transformed.shape) == 2 # should be (1, num_features)
    assert transformed[0, 0] == pytest.approx(0.0) # RecencyDays was 10 (min), so scaled to 0
