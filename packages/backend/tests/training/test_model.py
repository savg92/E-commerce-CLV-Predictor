import torch
import pytest

from backend.training import model


def test_mlp_forward_shape_and_layers():
    mlp_model = model.MLP(
        input_dim=8,
        hidden_dims=[16, 8],
        dropout=0.25,
        output_dim=1,
    )

    batch = torch.randn(4, 8)
    output = mlp_model(batch)

    assert output.shape == (4, 1)

    linear_layers = [module for module in mlp_model.network if isinstance(module, torch.nn.Linear)]
    dropout_layers = [module for module in mlp_model.network if isinstance(module, torch.nn.Dropout)]
    relu_layers = [module for module in mlp_model.network if isinstance(module, torch.nn.ReLU)]

    assert len(linear_layers) == 3
    assert len(dropout_layers) == 2
    assert len(relu_layers) == 2


def test_build_huber_loss_uses_requested_delta():
    loss_fn = model.build_huber_loss(delta=1.0)

    preds = torch.tensor([0.0, 2.0])
    targets = torch.tensor([0.0, 0.0])

    loss = loss_fn(preds, targets)

    assert isinstance(loss_fn, torch.nn.HuberLoss)
    assert loss.item() == pytest.approx(0.75)
