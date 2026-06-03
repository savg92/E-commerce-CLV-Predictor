import torch
from torch.utils.data import DataLoader, TensorDataset

from backend.training.model import MLP, build_huber_loss
from backend.training.loop import evaluate, train_one_epoch


def test_train_one_epoch_updates_model_parameters():
    torch.manual_seed(0)
    model = MLP(input_dim=8, hidden_dims=[4], dropout=0.0, output_dim=1)
    features = torch.randn(16, 8)
    targets = torch.randn(16, 1)
    loader = DataLoader(TensorDataset(features, targets), batch_size=4, shuffle=False)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    loss_fn = build_huber_loss(delta=1.0)

    before = [parameter.detach().clone() for parameter in model.parameters()]

    train_loss = train_one_epoch(model, loader, optimizer, loss_fn)

    after = list(model.parameters())
    assert train_loss >= 0.0
    assert any(not torch.equal(before_param, after_param) for before_param, after_param in zip(before, after))


def test_evaluate_returns_float_loss():
    model = MLP(input_dim=8, hidden_dims=[4], dropout=0.0, output_dim=1)
    features = torch.randn(8, 8)
    targets = torch.randn(8, 1)
    loader = DataLoader(TensorDataset(features, targets), batch_size=4, shuffle=False)
    loss_fn = build_huber_loss(delta=1.0)

    loss = evaluate(model, loader, loss_fn)

    assert isinstance(loss, float)
    assert loss >= 0.0
