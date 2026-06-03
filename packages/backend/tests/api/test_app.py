import os
import tempfile
from pathlib import Path

import joblib
import torch
from fastapi.testclient import TestClient

from backend.api.app import OOD_WARNING_TEXT, create_app, load_inference_bundle
from backend.training.data import build_training_split
from backend.training.model import MLP


def _write_sample_artifacts():
    lines = ["Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country"]

    for i in range(10):
        cust_id = f"1000{i}"
        lines.append(f"100{i},85123A,Prod,5,2009-12-05 10:00:00,2.5,{cust_id},UK")
        lines.append(f"101{i},85123A,Prod,2,2010-01-05 11:00:00,2.5,{cust_id},UK")
        lines.append(f"102{i},85123A,Prod,10,2010-10-05 12:00:00,3.0,{cust_id},UK")

    csv_content = "\n".join(lines)

    temp_csv = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
    temp_csv.write(csv_content)
    temp_csv.close()

    temp_dir = tempfile.TemporaryDirectory()
    split = build_training_split(temp_csv.name)
    model = MLP(input_dim=split.X_train.shape[1], hidden_dims=[4], dropout=0.0, output_dim=1)

    model_path = Path(temp_dir.name) / "best_model.pth"
    scaler_path = Path(temp_dir.name) / "scaler.joblib"
    torch.save(
        {
            "state_dict": model.state_dict(),
            "input_dim": split.X_train.shape[1],
            "hidden_dims": [4],
            "dropout": 0.0,
        },
        model_path,
    )
    joblib.dump(split.preprocessor, scaler_path)

    return temp_csv.name, temp_dir, model_path, scaler_path, split


def test_create_app_loads_inference_bundle_once():
    calls = []

    def fake_loader(model_path, scaler_path, ood_threshold=0.0):
        calls.append((model_path, scaler_path, ood_threshold))

        class DummyService:
            pass

        return DummyService()

    app = create_app(
        model_path=Path("/tmp/model.pth"),
        scaler_path=Path("/tmp/scaler.joblib"),
        bundle_loader=fake_loader,
    )

    with TestClient(app):
        assert len(calls) == 1
        assert app.state.inference_service is not None


def test_predict_endpoint_returns_prediction_and_ood_warning_for_outlier_input():
    csv_path, temp_dir, model_path, scaler_path, split = _write_sample_artifacts()
    try:
        app = create_app(model_path=model_path, scaler_path=scaler_path)
        with TestClient(app) as client:
            payload = split.train_frame.iloc[0][
                [
                    "Country",
                    "RecencyDays",
                    "TenureDays",
                    "Frequency",
                    "Monetary",
                    "AvgBasketValue",
                    "AvgBasketQuantity",
                    "UniqueProducts",
                    "AverageUnitPrice",
                ]
            ].to_dict()

            response = client.post("/predict", json=payload)
            assert response.status_code == 200
            body = response.json()
            assert isinstance(body["prediction"], float)
            assert body["ood"] is False
            assert body["warning"] is None
            assert body["anomaly_score"] == 0.0

            ood_payload = dict(payload)
            ood_payload["RecencyDays"] = 9999
            ood_payload["Monetary"] = 99999
            ood_payload["AvgBasketValue"] = 99999

            ood_response = client.post("/predict", json=ood_payload)
            assert ood_response.status_code == 200
            ood_body = ood_response.json()
            assert isinstance(ood_body["prediction"], float)
            assert ood_body["ood"] is True
            assert ood_body["warning"] == OOD_WARNING_TEXT
            assert ood_body["anomaly_score"] > 0.0
    finally:
        os.remove(csv_path)
        temp_dir.cleanup()


def test_predict_endpoint_rejects_invalid_payload():
    csv_path, temp_dir, model_path, scaler_path, _split = _write_sample_artifacts()
    try:
        app = create_app(model_path=model_path, scaler_path=scaler_path)
        with TestClient(app) as client:
            response = client.post(
                "/predict",
                json={
                    "RecencyDays": 10,
                    "TenureDays": 100,
                    "Frequency": 5,
                    "Monetary": 100.0,
                    "AvgBasketValue": 20.0,
                    "AvgBasketQuantity": 5.0,
                    "UniqueProducts": 10,
                    "AverageUnitPrice": 2.0,
                },
            )
            assert response.status_code == 422
    finally:
        os.remove(csv_path)
        temp_dir.cleanup()
