import datetime
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any, Optional
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from backend.domain.entities import Transaction

class FeaturePreprocessor:
    def __init__(self):
        self.numeric_features = [
            "RecencyDays",
            "TenureDays",
            "Frequency_log",
            "Monetary_log",
            "AvgBasketValue_log",
            "AvgBasketQuantity_log",
            "UniqueProducts_log",
            "AverageUnitPrice_log"
        ]
        self.categorical_features = ["Country"]
        
        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", MinMaxScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, self.numeric_features),
                ("cat", categorical_transformer, self.categorical_features),
            ]
        )

    def _prepare_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        log_cols = ["Frequency", "Monetary", "AvgBasketValue", "AvgBasketQuantity", "UniqueProducts", "AverageUnitPrice"]
        for col in log_cols:
            if col in df_copy.columns:
                # clip to 0 to prevent negative values in log1p
                df_copy[f"{col}_log"] = np.log1p(df_copy[col].clip(lower=0))
        
        # Ensure all numeric_features columns exist in dataframe (fill with NaN if missing so Imputer works)
        for col in self.numeric_features:
            if col not in df_copy.columns:
                df_copy[col] = np.nan
        for col in self.categorical_features:
            if col not in df_copy.columns:
                df_copy[col] = np.nan
                
        return df_copy

    def fit(self, df: pd.DataFrame):
        prepared = self._prepare_df(df)
        self.preprocessor.fit(prepared)
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        prepared = self._prepare_df(df)
        return self.preprocessor.transform(prepared)

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        prepared = self._prepare_df(df)
        return self.preprocessor.fit_transform(prepared)

    def transform_single(self, input_dict: Dict[str, Any]) -> np.ndarray:
        df = pd.DataFrame([input_dict])
        return self.transform(df)


class TemporalSplitter:
    @staticmethod
    def split_transactions(
        transactions: List[Transaction], 
        cutoff_date: datetime.datetime
    ) -> Tuple[List[Transaction], List[Transaction]]:
        obs = []
        future = []
        for t in transactions:
            if t.invoice_date <= cutoff_date:
                obs.append(t)
            else:
                future.append(t)
        return obs, future

    @staticmethod
    def split_train_val(
        customer_df: pd.DataFrame, 
        train_ratio: float = 0.8
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df_sorted = customer_df.sort_values("FirstPurchase").reset_index(drop=True)
        split_idx = int(len(df_sorted) * train_ratio)
        train = df_sorted.iloc[:split_idx].copy()
        val = df_sorted.iloc[split_idx:].copy()
        return train, val
