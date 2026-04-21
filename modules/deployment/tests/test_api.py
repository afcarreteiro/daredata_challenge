# Tests for the deployment prediction API.

import os
from pathlib import Path
import sys

os.environ["DEPLOYMENT_SKIP_MODEL_LOAD"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.deployment.api.app import create_app


class StubModel:
    def __init__(self) -> None:
        self.calls = []

    def predict_with_logging(self, client_idx, features):
        self.calls.append((client_idx, features.to_dict(orient="records")))
        return 1


def test_predict_returns_label_for_valid_request():
    model = StubModel()
    app = create_app(model=model)
    client = app.test_client()

    response = client.post(
        "/predict",
        json={
            "idx": 150000,
            "features": {
                "attr_a": 1,
                "attr_b": "c",
                "scd_a": 0.55,
                "scd_b": 3,
            },
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {"label": 1}
    assert model.calls == [
        (
            150000,
            [{"attr_a": 1, "attr_b": "c", "scd_a": 0.55, "scd_b": 3}],
        )
    ]


def test_predict_rejects_missing_features():
    app = create_app(model=StubModel())
    client = app.test_client()

    response = client.post(
        "/predict",
        json={
            "idx": 150000,
            "features": {
                "attr_a": 1,
                "attr_b": "c",
            },
        },
    )

    assert response.status_code == 400
    assert response.get_json()["missing_fields"] == ["scd_a", "scd_b"]
