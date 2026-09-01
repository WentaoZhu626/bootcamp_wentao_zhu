"""Flask API for the saved CSI 300 regime model."""

from __future__ import annotations

from pathlib import Path

import joblib
from flask import Flask, jsonify, request

from src.modeling import predict_features


PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "model" / "regime_model.joblib"


def create_app(model_path: str | Path = MODEL_PATH) -> Flask:
    """Create the application and load one immutable model artifact."""
    application = Flask(__name__)
    artifact = joblib.load(model_path)

    @application.get("/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "model_version": artifact["version"],
                "trained_through": artifact["trained_through"],
            }
        )

    @application.post("/predict")
    def predict():
        payload = request.get_json(silent=True) or {}
        features = payload.get("features")
        if not isinstance(features, dict):
            return jsonify({"error": "features must be a JSON object"}), 400
        try:
            return jsonify(predict_features(artifact, features))
        except (TypeError, ValueError) as error:
            return jsonify({"error": str(error)}), 400

    @application.get("/latest")
    def latest():
        return jsonify(predict_features(artifact, artifact["latest_features"]))

    return application


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5060)
