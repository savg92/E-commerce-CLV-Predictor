# E-commerce CLV Predictor

A deep learning-powered Customer Lifetime Value (CLV) prediction system that models future customer monetary value based on historical transaction behavior. The application features a FastAPI inference engine backend, an interactive React-Vite dashboard frontend, and a PyTorch training pipeline.

---

## Repository Structure

```text
.
├── Makefile                     # Root build and orchestration script
├── pyproject.toml               # Python project configuration (uv member packages)
├── bun.lock                     # Bun package lockfile
├── packages/
│   ├── backend/                 # Python backend
│   │   ├── Dockerfile
│   │   ├── src/backend/
│   │   │   ├── api/             # FastAPI routing and InferenceService
│   │   │   ├── domain/          # Core entities, use cases, and preprocessors
│   │   │   ├── infrastructure/  # Data loaders (CSV transaction repository)
│   │   │   └── training/        # PyTorch training, tuning sweeps, and RF baseline
│   │   └── tests/               # Backend PyTest suite (coverage > 85%)
│   └── frontend/                # Vite + React dashboard frontend
│       ├── Dockerfile
│       ├── src/                 # React components, stylesheets, and api client
│       └── src/App.tsx          # Interactive customer form and batch CSV loader
├── docs/                        # Project documentation
│   ├── api.md                   # REST API payload contracts
│   ├── architecture.md          # Architectural blueprints and diagrams
│   └── training_report.md       # Model tuning results and evaluation report
├── scripts/                     # Helper script utilities
│   ├── generate_placeholder_model.py  # Generates test model weights and preprocessors
│   └── expand_test_files.py
├── artifacts/                   # Persisted checkpoints (ignored in git)
│   └── training/                # Scalers and best_model.pth weight checkpoints
└── Test files/                  # CSV datasets for manual dashboard verification
```

---

## Table of Contents
1. [Setup & Onboarding](#setup--onboarding)
2. [Running the Application](#running-the-application)
3. [Training and Tuning Models](#training-and-tuning-models)
4. [Running Tests & Linting](#running-tests--linting)
5. [Architecture & API Documentation](#architecture--api-documentation)

---

## Setup & Onboarding

### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [bun](https://bun.sh/) (JavaScript package manager)
- [Docker](https://www.docker.com/) (for containerized deployments)

### Monorepo Setup
To configure virtual environments, synchronize python dependencies, and install node packages, execute:
```bash
make setup
```

---

## Running the Application

### 1. Using Docker (Recommended)
This runs the API on `http://localhost:8000` and the React frontend on `http://localhost:3000` in isolated containers:
```bash
docker compose up --build
```

### 2. Running Locally (Development Mode)
To run both the frontend and backend concurrently in watch mode locally:
```bash
make dev
```
Alternatively, you can run services individually:
- **Backend only:** `make dev-backend` (binds to port 8000)
- **Frontend only:** `make dev-frontend` (binds to port 5173)

---

## Training and Tuning Models

If you need to regenerate the scaling preprocessing artifacts or train new weights:

### 1. Generating Model Placeholders
A script is available to generate small-scale mock transactional datasets and run an immediate training sweep to persist new model weight checkpoints under `artifacts/training/`:
```bash
uv run scripts/generate_placeholder_model.py
```

### 2. Training the RandomForest Baseline
To run the domain RFM pipeline on a dataset and train the baseline RandomForest model:
```bash
PYTHONPATH=packages/backend/src uv run python packages/backend/src/backend/training/train_baseline.py --data-path <path_to_csv_or_excel>
```

---

## Running Tests & Linting

We enforce test coverage and syntax checks across both workspaces.

### Execute Test Suites
Runs backend unit tests (using Pytest with coverage reports) and frontend tests (using Vitest):
```bash
make test
```

### Format and Code Lints
Checks code formatting and imports (Ruff for python, TypeScript compiler check for TS/TSX):
```bash
make lint
```

### Documentation Verification
Validates internal document cross-references and header layouts:
```bash
make doc-lint
```

---

## Architecture & API Documentation
- **Architecture Details:** See [Detailed Architectural Blueprint](docs/architecture.md) for layers and inference flow.
- **REST Contracts:** See [API Contracts](docs/api.md) for payload definitions.
- **Training Analytics:** See [Training Metrics and Tuning Report](docs/training_report.md) for model parameters.

