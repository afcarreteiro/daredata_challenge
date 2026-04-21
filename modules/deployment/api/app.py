# Prediction API for serving the trained classification model.

from pathlib import Path
import os

from flask import Flask, jsonify, request
import pandas as pd

from data_science.modelling import SimpleModel


def load_model(model_dir: Path):
    """Load the trained DS model and its supporting artifacts."""

    model = SimpleModel()
    model.load(str(model_dir))
    return model


def create_app(model=None) -> Flask:
    """Build the Flask application with either a real or injected model."""

    app = Flask(__name__)
    runtime_model = model or load_model(
        Path(os.getenv("MODEL_DIR", "/app/models")).resolve()
    )

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/predict")
    def predict():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be valid JSON"}), 400

        idx = data.get("idx")
        features = data.get("features")

        if idx is None or not isinstance(features, dict):
            return (
                jsonify({"error": "Request must include 'idx' and 'features' fields"}),
                400,
            )

        required_features = {"attr_a", "attr_b", "scd_a", "scd_b"}
        missing_features = sorted(required_features - set(features))
        if missing_features:
            return (
                jsonify(
                    {
                        "error": "Missing required feature fields",
                        "missing_fields": missing_features,
                    }
                ),
                400,
            )

        label = runtime_model.predict_with_logging(
            idx,
            pd.DataFrame([features]),
        )

        return jsonify({"label": int(label)})

    return app



if __name__ == "__main__":

    app = None if os.getenv("DEPLOYMENT_SKIP_MODEL_LOAD") == "1" else create_app()
    if app is not None:
        app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
