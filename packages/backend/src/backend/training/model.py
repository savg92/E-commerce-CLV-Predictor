"""PyTorch model definitions for the CLV training pipeline."""

from __future__ import annotations

from collections.abc import Sequence

import torch
from torch import nn


class MLP(nn.Module):
    """Sequential multi-layer perceptron for CLV regression."""

    def __init__(
        self,
        input_dim: int,
        hidden_dims: Sequence[int],
        dropout: float = 0.0,
        output_dim: int = 1,
    ) -> None:
        super().__init__()

        if input_dim <= 0:
            raise ValueError("input_dim must be positive")
        if output_dim <= 0:
            raise ValueError("output_dim must be positive")
        if not 0.0 <= dropout < 1.0:
            raise ValueError("dropout must be in the range [0.0, 1.0)")
        if not hidden_dims:
            raise ValueError("hidden_dims must contain at least one layer size")

        layers: list[nn.Module] = []
        layer_dims = [input_dim, *hidden_dims, output_dim]

        for index, (in_features, out_features) in enumerate(
            zip(layer_dims[:-1], layer_dims[1:])
        ):
            layers.append(nn.Linear(in_features, out_features))

            is_last_layer = index == len(layer_dims) - 2
            if not is_last_layer:
                layers.append(nn.ReLU())
                if dropout > 0.0:
                    layers.append(nn.Dropout(p=dropout))

        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Run a forward pass through the MLP."""

        return self.network(x)


def build_huber_loss(delta: float = 1.0, reduction: str = "mean") -> nn.HuberLoss:
    """Create the robust loss function used by training."""

    if delta <= 0:
        raise ValueError("delta must be positive")

    return nn.HuberLoss(delta=delta, reduction=reduction)