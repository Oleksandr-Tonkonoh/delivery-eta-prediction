import os
import mlflow
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

mlflow_tracking_uri = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://localhost:5000",
).strip()

mlflow.set_tracking_uri(mlflow_tracking_uri)

MODEL_URI = "models:/delivery-eta-model/3"

mlflow_model = mlflow.pyfunc.load_model(MODEL_URI)


def predict_delivery_minutes(delivery_data: dict):
    df = pd.DataFrame([delivery_data])

    predicted_delivery_minutes = mlflow_model.predict(df)[0]

    return float(predicted_delivery_minutes)
