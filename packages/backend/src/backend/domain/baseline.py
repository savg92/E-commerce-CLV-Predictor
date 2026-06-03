import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict

class RandomForestBaseline:
    def __init__(self, n_estimators: int = 100, random_state: int = 42, **kwargs):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state, **kwargs)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RandomForestBaseline":
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {
        "mae": float(mae),
        "mse": float(mse),
        "r2": float(r2)
    }
