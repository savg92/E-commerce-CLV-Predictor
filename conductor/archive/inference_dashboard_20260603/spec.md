# Specification: FastAPI Inference API & React Dashboard

## Overview
Develop a real-time web application frontend and backend enabling users to input RFM data, invoke the PyTorch neural network model, and view predicted CLV values with integrated Out-of-Distribution (OOD) uncertainty management.

## Functional Requirements
- **Weights Management:** FastAPI app loads model `.pth` weights and preprocessing scaler into memory *only once* at startup utilizing `@asynccontextmanager lifespan`.
- **Inference Endpoints:** Create a POST endpoint `/predict` accepting RFM features, processing them via the scaler, and returning predicted CLV.
- **OOD Detection:** Calculate anomaly scores to verify if input data is an outlier relative to training data. Return OOD flag in prediction responses.
- **React Dashboard UI:** Build the React + TypeScript frontend dashboard with Bun. Styled with Tailwind CSS and Shadcn UI.
- **Inference Interface:** Support two ingestion methods:
  - CSV file upload for batch processing.
  - Interactive manual input form for single customer profile prediction.
- **Uncertainty Alert UI:** React frontend must catch the OOD flag and explicitly show warning: ⚠️ "Warning: I am not sure about this [prediction]!"

## Acceptance Criteria
- FastAPI server starts successfully and exposes `/predict` API.
- React frontend forms process manual input and CSV files, correctly rendering outputs and warning banners when OOD threshold is breached.
- End-to-end (E2E) integration tests via Playwright assert predictions against the live backend.
