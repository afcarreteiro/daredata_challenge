import time
from data_science.fetch_data import get_dataset
from data_science.modelling import SimpleModel
from sqlalchemy.exc import ProgrammingError


def main():
    "Fetches the data, trains and saves the model"
    # Very ugly "wait" functionality, until the feature_store table is online.
    # In a real production environment, the model training should be orchestrated as well!
    waiting = True
    while waiting:
        try:
            dataset = get_dataset()
            waiting = False
        except ProgrammingError:
            print("Does the feature_store table exist? Make sure you've run all the data ETLs", flush=True)
            time.sleep(5)
    
    # Instantiating and training the model
    print("Training the model...")
    model = SimpleModel()
    model.fit(dataset)
    model.save(model_folder="/models")
    print("Model saved and ready for deployment!")


if __name__ == "__main__":
    main()
    