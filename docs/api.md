# API Documentation - E-commerce CLV Predictor

The CLV Predictor API provides REST endpoints to estimate Customer Lifetime Value (CLV) based on RFM (Recency, Frequency, Monetary) features, as well as checking model inference boundaries via out-of-distribution (OOD) flagging.

## Endpoints

### 1. `/predict` (POST)

Predicts the future Customer Lifetime Value (CLV) for a single customer profile.

#### Request Payload (`PredictRequest`)
- `Country` (string): Country of the customer (e.g., `"United Kingdom"`).
- `RecencyDays` (float): Days since last purchase.
- `TenureDays` (float): Days since first purchase.
- `Frequency` (float): Total number of transactions.
- `Monetary` (float): Total monetary value of transactions.
- `AvgBasketValue` (float): Average value per invoice.
- `AvgBasketQuantity` (float): Average items per invoice.
- `UniqueProducts` (float): Number of unique products purchased.
- `AverageUnitPrice` (float): Average price per unit.

*Example Request (`application/json`):*
```json
{
  "Country": "United Kingdom",
  "RecencyDays": 15.0,
  "TenureDays": 320.0,
  "Frequency": 12.0,
  "Monetary": 450.50,
  "AvgBasketValue": 37.54,
  "AvgBasketQuantity": 15.2,
  "UniqueProducts": 25.0,
  "AverageUnitPrice": 2.45
}
```

#### Response Payload (`PredictResponse`)
- `prediction` (float): Predicted CLV (monetary value).
- `ood` (boolean): Out-of-Distribution flag. Triggered when input features exceed the normal range observed during training.
- `anomaly_score` (float): Score indicating anomaly level. Computed as the maximum value by which any feature exceeds the scaled interval `[0, 1]`.
- `warning` (string | null): Warning message if `ood` is true. Otherwise `null`.

*Example Response (Normal Input):*
```json
{
  "prediction": 850.75,
  "ood": false,
  "anomaly_score": 0.0,
  "warning": null
}
```

*Example Response (OOD Input):*
```json
{
  "prediction": 12450.20,
  "ood": true,
  "anomaly_score": 2.14,
  "warning": "Warning: I am not sure about this [prediction]!"
}
```

---

### 2. `/predict/batch` (POST)

Predicts the future Customer Lifetime Value (CLV) for an array of customer profiles.

#### Request Payload (`list[PredictRequest]`)
An array of customer profiles matching the `PredictRequest` schema.

*Example Request (`application/json`):*
```json
[
  {
    "Country": "United Kingdom",
    "RecencyDays": 10.0,
    "TenureDays": 100.0,
    "Frequency": 5.0,
    "Monetary": 100.0,
    "AvgBasketValue": 20.0,
    "AvgBasketQuantity": 5.0,
    "UniqueProducts": 10.0,
    "AverageUnitPrice": 2.0
  },
  {
    "Country": "Germany",
    "RecencyDays": 250.0,
    "TenureDays": 260.0,
    "Frequency": 1.0,
    "Monetary": 15.0,
    "AvgBasketValue": 15.0,
    "AvgBasketQuantity": 2.0,
    "UniqueProducts": 1.0,
    "AverageUnitPrice": 7.5
  }
]
```

#### Response Payload (`list[PredictResponse]`)
An array of predictions matching the `PredictResponse` schema in corresponding order.

*Example Response (`application/json`):*
```json
[
  {
    "prediction": 210.50,
    "ood": false,
    "anomaly_score": 0.0,
    "warning": null
  },
  {
    "prediction": 25.10,
    "ood": false,
    "anomaly_score": 0.0,
    "warning": null
  }
]
```

---

### 3. `/health` (GET)

Performs a simple API health check.

#### Response
- Returns `{"status": "ok"}` when the API is running and ready to accept inference requests.

