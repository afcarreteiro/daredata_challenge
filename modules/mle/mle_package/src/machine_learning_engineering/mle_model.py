from typing import Iterable, Any
import pandas as pd
from os.path import expanduser


class MLEModel():

	def load(self, *args, **kwargs) -> Any:
		"""
		Loads the model and any required artifacts.
		To be implemented by the data scientist.
		"""
		raise NotImplementedError()

	def save(self, *args, **kwargs) -> None:
		"""
		Saves the model and any required artifacts to a given location.
		To be implemented by the data scientist.
		"""
		raise NotImplementedError()

	def fit(self, data: Any):
		"""Fits the model to the data. To be implemented by the data scientist.
		"""
		raise NotImplementedError()

	def predict(self, features: Any) -> int:
		"""Predicts the label of unseen data. To be implemented by the data scientist.
		"""
		raise NotImplementedError()

	def predict_with_logging(self, client_idx: int, features: Any) -> None:
		"""
		Calls the predict function, implemented by the data scientist, and logs the results
		of the prediction to storage.
		"""
		predicted_label = self.predict(features)
		self.log_to_storage(client_idx, predicted_label)

		return predicted_label

	def log_to_storage(self, client_idx: int, predicted_label: int):
		"""
		Logs the prediction to the predictions table, on the database.
		Our extremely advanced "storage" is a text file on the `~/mle_storage` directory :-) 
		"""
		try:
			with open(f'{expanduser("~")}/mle_storage/labels', 'a+') as f:
				f.write(f"{client_idx},{predicted_label}\n")
		except FileNotFoundError:
			print("Have you created the ~/mle_storage directory?")
