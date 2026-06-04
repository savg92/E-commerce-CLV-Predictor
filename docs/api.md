# API Documentation - E-commerce CLV Predictor

## /predict (POST)
Predicts the future Customer Lifetime Value (CLV) based on RFM features.

### Request Payload (`PredictRequest`)
- `Country` (string): Country of the customer.
- `RecencyDays` (float): Days since last purchase.
- `TenureDays` (float): Days since first purchase.
- `Frequency` (float): Total number of transactions.
- `Monetary` (float): Total monetary value of transactions.
- `AvgBasketValue` (float): Average value per invoice.
- `AvgBasketQuantity` (float): Average items per invoice.
- `UniqueProducts` (float): Number of unique products purchased.
- `AverageUnitPrice` (float): Average price per unit.

### Response Payload (`PredictResponse`)
- `prediction` (float): Predicted CLV.
- `ood` (boolean): Out-of-Distribution flag.
- `anomaly_score` (float): Score indicating anomaly level.
- `warning` (string | null): Warning message if `ood` is true.

## /health (GET)
Check if the API is running.
- Returns: `{"status": "ok"}`
