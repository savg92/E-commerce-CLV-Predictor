# Implementation Plan: FastAPI Inference API & React Dashboard

## Phase 1: FastAPI Inference Backend

- [ ] Task: Create FastAPI app setup with lifespan context
    - [ ] Write unit test verifying model loading on app startup.
    - [ ] Setup FastAPI server configuration.
- [ ] Task: Develop `/predict` endpoint and OOD detection logic
    - [ ] Create unit tests validating `/predict` endpoint success and error conditions.
    - [ ] Implement preprocessing scaler load and forward propagation.
    - [ ] Implement anomaly checking calculation to output OOD warnings.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: FastAPI Inference Backend' (Protocol in workflow.md)

## Phase 2: React Dashboard UI

- [ ] Task: Create Dashboard Layout and Forms
    - [ ] Implement manual entry fields for RFM features.
    - [ ] Implement drag-and-drop CSV file loader for batch processing.
    - [ ] Write unit tests for form components using Vitest.
- [ ] Task: Implement OOD Alert Banner
    - [ ] Write frontend component styling and assertion for the warning: `Warning: I am not sure about this [prediction]!`.
    - [ ] Integrate endpoint fetch logic.
- [ ] Task: E2E Integration Testing
    - [ ] Configure Playwright to test end-to-end flow with actual backend connection.
    - [ ] Write and execute integration specs.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: React Dashboard UI' (Protocol in workflow.md)
