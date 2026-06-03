"""Training utilities for the CLV predictor backend."""

from .model import MLP, build_huber_loss

__all__ = ["MLP", "build_huber_loss"]
