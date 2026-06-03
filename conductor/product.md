# Initial Concept
The user wants to build an E-commerce Customer Lifetime Value (CLV) Predictor based on the existing `PRD.md`.

---

# Product Definition: E-commerce CLV Predictor

## Vision
To provide e-commerce businesses with a high-fidelity, deep learning-powered tool for predicting future Customer Lifetime Value (CLV). By leveraging non-linear relationships in transactional data (RFM), the system enables marketing teams and analysts to optimize retention strategies and ad spend with confidence.

## Target Audience
- **Marketing Teams:** Focused on optimizing ad spend and retention campaigns.
- **Data Analysts:** Interested in exploring customer behavior patterns and model performance.
- **E-commerce Owners:** Seeking a high-level view of business health and customer value.

## Core Objectives
- **Predict Future CLV:** Accurately model the relationship between historical RFM metrics and future monetary value.
- **Model Accuracy:** Utilize Deep Learning (PyTorch MLP) to capture non-linearities that traditional models miss.
- **Actionable Insights:** Provide a user-friendly interface for real-time inference and uncertainty management.

## Key Features
- **RFM Analytics:** Automated engineering of Recency, Frequency, and Monetary features from transactional logs.
- **Deep Learning Modeling:** Sequential MLP architecture optimized with Huber Loss for robustness against outliers.
- **Uncertainty Management:** Integrated Out-of-Distribution (OOD) detection with UI alerts for low-confidence predictions.
- **Flexible Data Ingestion:**
  - **CSV Upload:** Batch processing of historical transaction data.
  - **Manual Input:** Real-time prediction for individual customer profiles via a simple form.
  - **DB Integration:** Scalable connection to production data sources for automated monitoring.

## Success Metrics
- Performance gain over standard linear regression baselines.
- Successful deployment of a functional web prototype (FastAPI + React).
- User ability to distinguish high-confidence predictions from OOD outliers.
