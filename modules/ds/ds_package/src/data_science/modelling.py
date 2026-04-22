from machine_learning_engineering.mle_model import MLEModel
import autosklearn.classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pickle
from pathlib import Path
from datetime import datetime
from typing import Any
import pandas as pd


class SimpleModel(MLEModel):
    ohe = None         # one-hot encoder for categorical features
    model = None       # the model itself

    def _get_latest_artifact_paths(self, model_folder: str) -> tuple[Path, Path]:
        model_dir = Path(model_folder)
        model_files = sorted(model_dir.glob("model_*.pkl"), reverse=True)

        for model_path in model_files:
            timestamp = model_path.stem.removeprefix("model_")
            ohe_path = model_dir / f"one_hot_encoder_{timestamp}.pkl"
            if ohe_path.exists():
                return model_path, ohe_path

        return model_dir / "model.pkl", model_dir / "one_hot_encoder.pkl"

    def load(self, model_folder) -> Any:
        """Loads the model to memory. To be implemented by the data scientist.
        """
        model_path, ohe_path = self._get_latest_artifact_paths(model_folder)

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
        with open(ohe_path, "rb") as f:
            self.ohe = pickle.load(f)

    def save(self, model_folder) -> None:
        """Saves the model to a given location. To be implemented by the data scientist.
        """
        model_dir = Path(model_folder)
        model_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

        with open(model_dir / f"model_{timestamp}.pkl", "wb") as f:
            pickle.dump(self.model, f)
        with open(model_dir / f"one_hot_encoder_{timestamp}.pkl", "wb") as f:
            pickle.dump(self.ohe, f)

    def _one_hot_encode(self, dataset: pd.DataFrame):
        """One-hot encodes the categorical features in the dataset.
        """
        categorical_columns = dataset.select_dtypes(['category', object]).columns
        dummies = pd.DataFrame(self.ohe.fit_transform(dataset[categorical_columns]).toarray(), 
                            index=dataset.index, 
                            dtype=int)

        df_ohe = pd.concat([dataset.drop(categorical_columns, axis=1), dummies], axis=1)

        return df_ohe

    def fit(self, dataset: Any) -> dict:
        """
        Fits the model to the data. To be implemented by the data scientist.
        
        Note: For the purpose of this test, and since we are lazy, we are using a very simple
        AutoML approach, without any metrics reporting or care whatsoever :-) 

        NEVER do this on an actual project!!
        """
        # One hot encoding the categorical features.
        self.ohe = OneHotEncoder(handle_unknown='ignore')
        df_ohe = self._one_hot_encode(dataset)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(df_ohe.drop("label", axis=1), dataset["label"], test_size=0.33, random_state=42)

        # Training as fast as possible!
        self.model = autosklearn.classification.AutoSklearnClassifier(
            time_left_for_this_task=30, # training will take 30 seconds :-)
            ensemble_size=5,
            ensemble_nbest=5
        )
        self.model.fit(X_train, y_train)

    def predict(self, features: pd.DataFrame) -> int:
        """Predicts the label of unseen data. To be implemented by the data scientist.
        """
        features_ohe = self._one_hot_encode(features)
        label = self.model.predict(features_ohe)[0]
        
        return label
