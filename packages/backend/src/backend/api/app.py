"""FastAPI inference application for the CLV predictor."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import joblib
import numpy as np
import torch
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from backend.training.model import MLP


OOD_WARNING_TEXT = "Warning: I am not sure about this [prediction]!"
DEFAULT_MODEL_PATH = Path("artifacts/training/best_model.pth")
DEFAULT_SCALER_PATH = Path("artifacts/training/scaler.joblib")


class PredictRequest(BaseModel):
    """RFM-style feature payload accepted by the inference API."""

    Country: str
    RecencyDays: float
    TenureDays: float
    Frequency: float
    Monetary: float
    AvgBasketValue: float
    AvgBasketQuantity: float
    UniqueProducts: float
    AverageUnitPrice: float


class PredictResponse(BaseModel):
    """Prediction response returned by the inference API."""

    prediction: float
    ood: bool
    anomaly_score: float
    warning: str | None = None


@dataclass(slots=True)
class InferenceService:
    """Model bundle plus helper logic for a single prediction."""

    model: MLP
    preprocessor: object
    ood_threshold: float = 0.0

    def predict(self, payload: PredictRequest) -> PredictResponse:
        """Generate a prediction and OOD assessment for one customer profile."""

        scaled_features = np.asarray(self.preprocessor.transform_single(payload.model_dump()), dtype=float)
        excess_below = np.clip(-scaled_features, a_min=0.0, a_max=None)
        excess_above = np.clip(scaled_features - 1.0, a_min=0.0, a_max=None)
        anomaly_score = float(max(excess_below.max(), excess_above.max()))
        ood = anomaly_score > self.ood_threshold

        self.model.eval()
        with torch.no_grad():
            tensor = torch.tensor(scaled_features, dtype=torch.float32)
            prediction = float(self.model(tensor).squeeze().item())

        return PredictResponse(
            prediction=prediction,
            ood=ood,
            anomaly_score=anomaly_score,
            warning=OOD_WARNING_TEXT if ood else None,
        )


def load_inference_bundle(
    model_path: str | Path,
    scaler_path: str | Path,
    ood_threshold: float = 0.0,
) -> InferenceService:
    """Load the model checkpoint and preprocessing scaler into memory."""

    checkpoint = torch.load(Path(model_path), map_location="cpu")
    model = MLP(
        input_dim=int(checkpoint["input_dim"]),
        hidden_dims=list(checkpoint["hidden_dims"]),
        dropout=float(checkpoint["dropout"]),
        output_dim=1,
    )
    model.load_state_dict(checkpoint["state_dict"])
    preprocessor = joblib.load(Path(scaler_path))
    return InferenceService(model=model, preprocessor=preprocessor, ood_threshold=ood_threshold)


def create_app(
    model_path: str | Path | None = None,
    scaler_path: str | Path | None = None,
    ood_threshold: float = 0.0,
    bundle_loader: Callable[[str | Path, str | Path, float], InferenceService] = load_inference_bundle,
) -> FastAPI:
    """Create the FastAPI application with lifespan-managed model loading."""

    final_model_path = model_path or os.environ.get("MODEL_PATH", DEFAULT_MODEL_PATH)
    final_scaler_path = scaler_path or os.environ.get("SCALER_PATH", DEFAULT_SCALER_PATH)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.inference_service = bundle_loader(final_model_path, final_scaler_path, ood_threshold)
        yield

    app = FastAPI(title="E-commerce CLV Predictor", lifespan=lifespan)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/predict", response_model=PredictResponse)
    def predict(payload: PredictRequest, request: Request) -> PredictResponse:
        service = getattr(request.app.state, "inference_service", None)
        if service is None:
            raise HTTPException(status_code=503, detail="Inference service is not initialized.")
        return service.predict(payload)

    return app
