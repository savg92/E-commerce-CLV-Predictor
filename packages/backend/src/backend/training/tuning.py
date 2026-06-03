"""Hyperparameter tuning orchestration for the PyTorch CLV model."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import joblib
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from backend.training.data import TrainingSplit, build_training_split
from backend.training.loop import evaluate, train_one_epoch
from backend.training.model import MLP, build_huber_loss


@dataclass(frozen=True, slots=True)
class HyperparameterTrial:
    """A single tuning configuration and its final losses."""

    learning_rate: float
    dropout: float
    dense_units: int
    train_loss: float
    val_loss: float


@dataclass(frozen=True, slots=True)
class HyperparameterSearchResult:
    """The outcome of a hyperparameter sweep."""

    best_config: HyperparameterTrial
    best_weights_path: Path
    scaler_path: Path
    history: list[HyperparameterTrial]


def _set_seed(seed: int) -> None:
    """Seed all random number generators used by tuning."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def _build_dataloaders(
    split: TrainingSplit,
    batch_size: int,
    seed: int,
) -> tuple[DataLoader, DataLoader]:
    """Create deterministic train/validation data loaders from a bundle."""

    train_features = torch.tensor(np.array(split.X_train, copy=True), dtype=torch.float32)
    train_targets = torch.tensor(np.array(split.y_train, copy=True), dtype=torch.float32).unsqueeze(-1)
    val_features = torch.tensor(np.array(split.X_val, copy=True), dtype=torch.float32)
    val_targets = torch.tensor(np.array(split.y_val, copy=True), dtype=torch.float32).unsqueeze(-1)

    generator = torch.Generator().manual_seed(seed)
    train_loader = DataLoader(
        TensorDataset(train_features, train_targets),
        batch_size=batch_size,
        shuffle=True,
        generator=generator,
    )
    val_loader = DataLoader(
        TensorDataset(val_features, val_targets),
        batch_size=batch_size,
        shuffle=False,
    )
    return train_loader, val_loader


def run_hyperparameter_search(
    data_path: str,
    learning_rates: Sequence[float],
    dropout_rates: Sequence[float],
    dense_units: Sequence[int],
    epochs: int = 5,
    batch_size: int = 32,
    output_dir: str | Path = "artifacts/training",
    seed: int = 42,
) -> HyperparameterSearchResult:
    """Run a small grid search and persist the best model artifacts."""

    if epochs <= 0:
        raise ValueError("epochs must be positive")
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    if not learning_rates or not dropout_rates or not dense_units:
        raise ValueError("All hyperparameter grids must contain at least one value")

    _set_seed(seed)

    split = build_training_split(data_path)
    train_loader, val_loader = _build_dataloaders(split, batch_size=batch_size, seed=seed)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    weights_path = output_path / "best_model.pth"
    scaler_path = output_path / "scaler.joblib"

    input_dim = split.X_train.shape[1]
    loss_fn = build_huber_loss()
    history: list[HyperparameterTrial] = []
    best_trial: HyperparameterTrial | None = None
    best_val_loss = float("inf")

    for learning_rate in learning_rates:
        for dropout in dropout_rates:
            for units in dense_units:
                _set_seed(seed)
                model = MLP(
                    input_dim=input_dim,
                    hidden_dims=[units],
                    dropout=dropout,
                    output_dim=1,
                )
                optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

                train_loss = 0.0
                val_loss = 0.0
                for _ in range(epochs):
                    train_loss = train_one_epoch(model, train_loader, optimizer, loss_fn)
                    val_loss = evaluate(model, val_loader, loss_fn)

                trial = HyperparameterTrial(
                    learning_rate=learning_rate,
                    dropout=dropout,
                    dense_units=units,
                    train_loss=train_loss,
                    val_loss=val_loss,
                )
                history.append(trial)

                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    best_trial = trial
                    torch.save(
                        {
                            "state_dict": model.state_dict(),
                            "input_dim": input_dim,
                            "hidden_dims": [units],
                            "dropout": dropout,
                        },
                        weights_path,
                    )
                    joblib.dump(split.preprocessor, scaler_path)

    if best_trial is None:
        raise RuntimeError("No hyperparameter trials were executed")

    return HyperparameterSearchResult(
        best_config=best_trial,
        best_weights_path=weights_path,
        scaler_path=scaler_path,
        history=history,
    )