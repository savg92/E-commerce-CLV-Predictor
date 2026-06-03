"""Training and evaluation loops for PyTorch model optimization."""

from __future__ import annotations

from collections.abc import Iterable

import torch
from torch import nn


def _resolve_device(model: nn.Module, device: str | torch.device | None = None) -> torch.device:
    """Return the device that should be used for loop execution."""

    if device is not None:
        return torch.device(device)

    return next(model.parameters()).device


def train_one_epoch(
    model: nn.Module,
    dataloader: Iterable[tuple[torch.Tensor, torch.Tensor]],
    optimizer: torch.optim.Optimizer,
    loss_fn: nn.Module,
    device: str | torch.device | None = None,
) -> float:
    """Run a single training epoch and return the average loss."""

    resolved_device = _resolve_device(model, device)
    model.train()

    total_loss = 0.0
    total_examples = 0

    for features, targets in dataloader:
        features = features.to(resolved_device).float()
        targets = targets.to(resolved_device).float()

        optimizer.zero_grad(set_to_none=True)
        predictions = model(features)
        loss = loss_fn(predictions, targets)
        loss.backward()
        optimizer.step()

        batch_size = features.shape[0]
        total_loss += loss.item() * batch_size
        total_examples += batch_size

    average_loss = total_loss / total_examples if total_examples else 0.0
    print(f"Training loss: {average_loss:.4f}")
    return float(average_loss)


@torch.no_grad()
def evaluate(
    model: nn.Module,
    dataloader: Iterable[tuple[torch.Tensor, torch.Tensor]],
    loss_fn: nn.Module,
    device: str | torch.device | None = None,
) -> float:
    """Evaluate a model and return the average loss."""

    resolved_device = _resolve_device(model, device)
    model.eval()

    total_loss = 0.0
    total_examples = 0

    for features, targets in dataloader:
        features = features.to(resolved_device).float()
        targets = targets.to(resolved_device).float()

        predictions = model(features)
        loss = loss_fn(predictions, targets)

        batch_size = features.shape[0]
        total_loss += loss.item() * batch_size
        total_examples += batch_size

    average_loss = total_loss / total_examples if total_examples else 0.0
    print(f"Validation loss: {average_loss:.4f}")
    return float(average_loss)