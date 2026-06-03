# Implementation Plan: FastAPI Inference API & React Dashboard

## Project Hardening Rules

- Load model weights and preprocessors once at startup and document that lifecycle clearly.
- Keep the `/predict` response schema stable so the frontend and E2E tests remain reliable.
- Surface the OOD warning string exactly as required by the product guideline.
- Require live-backend verification for any end-to-end dashboard change.
- Never expose inference behavior that assumes a different preprocessing contract than training.

## Phase 1: FastAPI Inference Backend [checkpoint: bddabbd]

- [x] Task: Create FastAPI app setup with lifespan context
  - [x] Write unit test verifying model loading on app startup.
  - [x] Setup FastAPI server configuration.
        _Summary:_ Added a lifespan-managed `create_app()` factory that loads the model bundle once on startup and exposes a health endpoint for readiness checks.
- [x] Task: Develop `/predict` endpoint and OOD detection logic
  - [x] Create unit tests validating `/predict` endpoint success and error conditions.
  - [x] Implement preprocessing scaler load and forward propagation.
  - [x] Implement anomaly checking calculation to output OOD warnings.
        _Summary:_ Added `/predict` with typed request/response models, single-pass preprocessing, model inference, and OOD detection that surfaces the exact warning text when inputs exceed the training scaling range.
- [x] Task: Conductor - User Manual Verification 'Phase 1: FastAPI Inference Backend' (Protocol in workflow.md)
  _Summary:_ Verified the backend with the targeted API tests and the full monorepo test target. Confirmed the inference app boots via lifespan startup, loads the bundle once, and returns prediction/OOD payloads as expected.

## Phase 2: React Dashboard UI

- [x] Task: Create Dashboard Layout and Forms
  - [x] Implement manual entry fields for RFM features.
  - [x] Implement drag-and-drop CSV file loader for batch processing.
  - [x] Write unit tests for form components using Vitest.
        _Summary:_ Added a React dashboard shell with a manual RFM form, CSV upload preview, and a prediction summary card. Covered the inputs and CSV flow with Vitest + Testing Library tests.
- [x] Task: Implement OOD Alert Banner
  - [x] Write frontend component styling and assertion for the warning: `Warning: I am not sure about this [prediction]!`.
  - [x] Integrate endpoint fetch logic.
        _Summary:_ Wired the dashboard to display the exact OOD warning banner when the backend response sets `ood: true`, and styled the banner with the product's amber alert treatment.
- [~] Task: E2E Integration Testing
  - [ ] Configure Playwright to test end-to-end flow with actual backend connection.
  - [ ] Write and execute integration specs.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: React Dashboard UI' (Protocol in workflow.md)
