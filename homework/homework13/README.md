# Stage 13 Homework - Prediction API

This Flask API serves predictions from a two-feature linear regression model trained on a deterministic synthetic dataset. The model is loaded once when the application starts and is reused by both prediction routes.

## Install dependencies

    python -m pip install scikit-learn joblib flask requests

## Running it

    python app.py

The server starts on http://127.0.0.1:5055 and loads `model/model.pkl` at startup.

## POST /predict

    curl -X POST http://127.0.0.1:5055/predict          -H "Content-Type: application/json"          -d '{"features": [0.1, 0.2]}'

Response: `{"prediction":23.58961171297328}`

## GET /predict/<f1>/<f2>

    curl http://127.0.0.1:5055/predict/0.1/0.2

Response: `{"prediction":23.58961171297328}`

## Bad input

Missing features, the wrong number of features, nonnumeric JSON values, or nonnumeric path parameters return HTTP 400 with a JSON error. Example: `{"error":"f1 and f2 must be numbers"}`
