# Product Requirements Document (PRD)
**Project Name:** E-commerce Customer Lifetime Value (CLV) Predictor  
**Program:** Non-Linear Regressions  
**Status:** Active  
**Version:** 1.0.0  

## Table of Contents
1. [Project Overview & Objectives](#1-project-overview--objectives)
2. [System Architecture & Tech Stack](#2-system-architecture--tech-stack)
3. [Phase 0: Data Engineering & Baseline (Pre-Entrega)](#3-phase-0-data-engineering--baseline-pre-entrega)
4. [Phase I: Deep Learning Implementation](#4-phase-i-deep-learning-implementation)
5. [Phase II: Application Core & Inference Engine](#5-phase-ii-application-core--inference-engine)
6. [DevOps, Testing & Deployment](#6-devops-testing--deployment)
7. [Academic Deliverables](#7-academic-deliverables)

---

## 1. Project Overview & Objectives
The objective of this project is to model the complex, non-linear relationship between a customer's historical transactional behavior and their future monetary value (Customer Lifetime Value). 

Unlike linear models that assume constant decay, this system utilizes Deep Learning to capture non-linear interactions between variables such as Recency, Frequency, and Monetary (RFM) value.

*   **Primary Academic Goal:** Fulfill and exceed the requirements for Unit 5: Non-Linear Regressions.
*   **Dataset:** [Online Retail II (UCI)](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II) — A two-year transactional dataset from a UK-based online retailer (2009-2011).
*   **Business Value:** Provide actionable, predictive intelligence for marketing optimization based on real-world transactional data.

---

## 2. System Architecture & Tech Stack
The project is organized as a **modern monorepo**, ensuring seamless integration between Data Science workflows and software engineering pipelines.

### Tech Stack
*   **Environment Management:** `uv` Workspaces (Python) & `bun` (JavaScript/TypeScript).
*   **Orchestration:** `make` for centralized task execution (e.g., `make train`, `make dev`, `make test`).
*   **Machine Learning:** PyTorch, Scikit-Learn, Pandas.
*   **Backend:** FastAPI (Python).
*   **Frontend:** React + Vite, Shadcn UI, Tailwind CSS.
*   **Testing:** Vitest (Frontend unit testing), Playwright (End-to-End testing).
*   **Infrastructure/DevOps:** Docker, Kubernetes (AWS), Vercel.

---

## 3. Phase 0: Data Engineering & Baseline (Pre-Entrega)
This phase serves as the foundation and is delivered as a functional Jupyter Notebook (`pre_entrega.ipynb`). 

### Data Processing Pipeline
1.  **EDA & Cleansing:** Distribution analysis, correlation heatmaps, handling missing `CustomerID`s, and filtering extreme outliers ("whales").
2.  **Temporal Feature Engineering:** Strict chronological splitting to prevent data leakage. 
    *   *Observation Window (e.g., Months 1-9):* Used to calculate RFM features ($X$).
    *   *Target Window (e.g., Months 10-12):* Used to define the true future CLV target ($y$).
3.  **Data Transformation:** 
    *   **Log-Transform:** Applied to Monetary and Frequency metrics (`np.log1p`) to handle heavy right-skewed financial distributions.
    *   **Scaling:** Post-log Min-Max Scaling (0-1 range) to prepare inputs for neural network optimization.
4.  **Baseline Modeling:** A `RandomForestRegressor` is trained as a non-linear tabular baseline to benchmark the performance gains of the deep learning model.
5.  **Partitioning:** A mandatory 80/20 Train/Validation split to monitor loss and prevent overfitting.

---

## 4. Phase I: Deep Learning Implementation
The final modeling logic transitions from notebooks to a production-ready Python script (`training/train_final.py`).

### Neural Network Architecture
*   **Framework:** PyTorch.
*   **Topology:** Sequential Multi-Layer Perceptron (MLP).
*   **Layers:** Multiple Dense (Linear) layers combined with **ReLU** activations to capture non-linearities, and **Dropout** layers for regularization.
*   **Loss Function:** **Huber Loss**. Chosen over standard MSE because it is significantly more robust to financial data outliers, acting as MSE for small errors and Mean Absolute Error (MAE) for larger ones.
*   **Hyperparameter Grid:** Automated tuning for:
    *   Learning Rates ($0.001$, $0.0001$)
    *   Dropout Rates ($0.2$, $0.3$)
    *   Dense Unit capacity ($256$, $1024$)

---

## 5. Phase II: Application Core & Inference Engine
A functional web prototype serves as a Proof of Concept (PoC) for real-time model inference.

### Backend Logic (FastAPI)
*   **State Management:** To prevent memory bottlenecks, the PyTorch `.pth` weights are loaded into application memory *only once* during server startup utilizing FastAPI's `@asynccontextmanager lifespan`.
*   **Inference API:** Accepts user-input RFM features, applies the exact preprocessing scaler used in training, and returns the predicted future CLV.

### Frontend Logic & Uncertainty Management
*   **Out-of-Distribution (OOD) Safety Mechanism:** The backend calculates if the input data represents an outlier compared to the training distribution. 
*   **UI Requirement:** If the user inputs data that triggers the OOD threshold, the React frontend must explicitly display the alert: 
    > ⚠️ **"Warning: I am not sure about this [prediction]!"**

---

## 6. DevOps, Testing & Deployment
The system is built to standard industry deployment protocols, making it cloud-agnostic and highly scalable.

### Deployment Strategy
*   **Backend (API + ML Model):** Containerized using **Docker**. Capable of being deployed to cloud environments like AWS ECS or highly scalable **Kubernetes (K8s)** clusters.
*   **Frontend (UI):** Optimized as a static build and deployed to edge networks via **Vercel**.

### Testing Suite
*   **Unit Tests:** Handled by `Vitest` to ensure frontend logic and state management work flawlessly.
*   **E2E Tests:** `Playwright` is configured to run end-to-end user flows against the **Live Development Backend**. This ensures full integration testing of the PyTorch inference pipeline, proving the system works with real predictions, rather than relying on mocked data.

---

## 7. Academic Deliverables
To meet the strict "Documentación técnico funcional" standards of the academic program, the final submission will include:
1.  **Source Code:** Fully commented monorepo accessible via GitHub.
2.  **Jupyter Notebook:** The Phase 0 `pre_entrega.ipynb` showing the EDA, preprocessing, and baseline.
3.  **Training Metrics:** Documented training history (loss curves over epochs).
4.  **Tuning Report:** Results and justification of the hyperparameter tuning grid.
5.  **Live Prototype:** The deployed (or locally deployable via `make dev`) React + FastAPI application demonstrating real-time inference and uncertainty handling.