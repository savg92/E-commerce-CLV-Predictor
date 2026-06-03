"""Baseline modeling for the E-commerce CLV Predictor."""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict

class RandomForestBaseline:
    """A wrapper for the RandomForestRegressor to establish a performance baseline.
    """

    def __init__(self, n_estimators: int = 100, random_state: int = 42, **kwargs):
        """Initializes the RandomForestBaseline."""
        self.model = RandomForestRegressor(
            n_estimators=n_estimators, random_state=random_state, **kwargs
        )

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RandomForestBaseline":
        """Fits the model to the training data.

        Args:
            X: Feature matrix.
            y: Target vector.

        Returns:
            The fitted RandomForestBaseline instance.
        """
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generates predictions for the given features.

        Args:
            X: Feature matrix.

        Returns:
            An array of predictions.
        """
        return self.model.predict(X)

def evaluate_predictions(
    y_true: np.ndarray, 
    y_pred: np.ndarray
) -> Dict[str, float]:
    """Calculates evaluation metrics for the predictions.

    Args:
        y_true: Ground truth target values.
        y_pred: Predicted target values.

    Returns:
        A dictionary containing MAE, MSE, and R2 scores.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {
        "mae": float(mae),
        "mse": float(mse),
        "r2": float(r2)
    }
