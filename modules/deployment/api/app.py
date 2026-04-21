# PSEUDOCODE!
# Requires the pip-installable DS and MLE modules...
import ...
from data_science.modelling import SimpleModel

MODEL = SimpleModel()
MODEL.load('<path to models folder>')

app = ...

@app.route("/predict", methods=...)
def predict():
    data = request.json

    label = MODEL.predict_with_logging(
        data["idx"],
        pd.DataFrame([data["features"]])
    )

    return {"label": int(label)}
