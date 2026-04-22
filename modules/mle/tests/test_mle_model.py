import logging
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "modules" / "mle" / "mle_package" / "src"))

from machine_learning_engineering.mle_model import MLEModel


class StubModel(MLEModel):
    def predict(self, features):
        return 1


def test_predict_with_logging_logs_to_file_and_persists_prediction(
    tmp_path, monkeypatch, caplog
):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    (tmp_path / "mle_storage").mkdir()

    model = StubModel()

    with caplog.at_level(logging.INFO):
        predicted_label = model.predict_with_logging(123, {"feature": "value"})

    assert predicted_label == 1
    assert (tmp_path / "mle_storage" / "labels").read_text() == "123,1\n"
    log_file = tmp_path / "mle_storage" / "logging" / "mle.log"
    assert log_file.exists()
    assert "Predicting label for client_idx=123" in log_file.read_text()
    assert "Prediction stored for client_idx=123 with predicted_label=1" in log_file.read_text()
    assert "Predicting label for client_idx=123" in caplog.text
    assert "Prediction stored for client_idx=123 with predicted_label=1" in caplog.text


def test_predict_with_logging_does_not_duplicate_file_handlers(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    (tmp_path / "mle_storage").mkdir()

    model = StubModel()
    model.predict_with_logging(123, {"feature": "value"})
    model.predict_with_logging(456, {"feature": "value"})

    log_text = (tmp_path / "mle_storage" / "logging" / "mle.log").read_text()

    assert log_text.count("Predicting label for client_idx=123") == 1
    assert log_text.count("Prediction stored for client_idx=123 with predicted_label=1") == 1
    assert log_text.count("Predicting label for client_idx=456") == 1
    assert log_text.count("Prediction stored for client_idx=456 with predicted_label=1") == 1
