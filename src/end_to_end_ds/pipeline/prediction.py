import joblib 
import pandas as pd
import numpy as np
from pathlib import Path


class PredictionPipeline:
    def __init__(self):
        self.model = joblib.load(Path("artifacts/model_trainer/model.joblib"))

    def predict(self, data: pd.DataFrame):
        return self.model.predict(data)