import logging
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "modules" / "mle" / "mle_package" / "src"))

from machine_learning_engineering.mle_model import MLEModel


class StubModel(MLEModel):
    def predict(self, features):
        return 1


def test_predict_with_logging_logs_and_persists_prediction(tmp_path, monkeypatch, caplog):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    (tmp_path / "mle_storage").mkdir()

    model = StubModel()

    with caplog.at_level(logging.INFO):
        predicted_label = model.predict_with_logging(123, {"feature": "value"})

    assert predicted_label == 1
    assert (tmp_path / "mle_storage" / "labels").read_text() == "123,1\n"
    assert "Predicting label for client_idx=123" in caplog.text
    assert "Prediction stored for client_idx=123 with predicted_label=1" in caplog.text
