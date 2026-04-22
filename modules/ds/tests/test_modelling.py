import sys
import time
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "modules" / "mle" / "mle_package" / "src"))
sys.path.insert(0, str(ROOT / "modules" / "ds" / "ds_package" / "src"))

autosklearn_module = types.ModuleType("autosklearn")
classification_module = types.ModuleType("autosklearn.classification")
classification_module.AutoSklearnClassifier = object
autosklearn_module.classification = classification_module
sys.modules.setdefault("autosklearn", autosklearn_module)
sys.modules.setdefault("autosklearn.classification", classification_module)

sklearn_module = types.ModuleType("sklearn")
model_selection_module = types.ModuleType("sklearn.model_selection")
preprocessing_module = types.ModuleType("sklearn.preprocessing")
model_selection_module.train_test_split = object
preprocessing_module.OneHotEncoder = object
sklearn_module.model_selection = model_selection_module
sklearn_module.preprocessing = preprocessing_module
sys.modules.setdefault("sklearn", sklearn_module)
sys.modules.setdefault("sklearn.model_selection", model_selection_module)
sys.modules.setdefault("sklearn.preprocessing", preprocessing_module)

from data_science.modelling import SimpleModel


def test_save_uses_timestamped_filenames_and_loads_latest(tmp_path):
    first_model = SimpleModel()
    first_model.model = {"version": 1}
    first_model.ohe = {"encoder": 1}
    first_model.save(tmp_path)

    time.sleep(0.01)

    second_model = SimpleModel()
    second_model.model = {"version": 2}
    second_model.ohe = {"encoder": 2}
    second_model.save(tmp_path)

    saved_files = sorted(path.name for path in tmp_path.iterdir())

    assert len(saved_files) == 4
    assert all(name.endswith(".pkl") for name in saved_files)
    assert any(name.startswith("model_") for name in saved_files)
    assert any(name.startswith("one_hot_encoder_") for name in saved_files)

    loaded_model = SimpleModel()
    loaded_model.load(tmp_path)

    assert loaded_model.model == {"version": 2}
    assert loaded_model.ohe == {"encoder": 2}
