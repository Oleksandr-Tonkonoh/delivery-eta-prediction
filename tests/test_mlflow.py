import os

import mlflow
import pandas as pd
import pytest


@pytest.fixture
def mlflow_model():
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)

    try:
        return mlflow.pyfunc.load_model("models:/delivery-eta-model/3")
    except Exception as exc:
        pytest.skip(f"MLflow integration environment is unavailable: {exc}")


def test_mlflow_model_load(mlflow_model):
    assert mlflow_model is not None


def test_mlflow_prediction(mlflow_model, delivery):
    df = pd.DataFrame([delivery])

    prediction = mlflow_model.predict(df)[0]

    assert prediction > 0
    assert isinstance(float(prediction), float)


def test_mlflow_matches_joblib(mlflow_model, joblib_model, delivery):
    df = pd.DataFrame([delivery])

    mlflow_prediction = mlflow_model.predict(df)[0]
    joblib_prediction = joblib_model.predict(df)[0]

    assert mlflow_prediction == pytest.approx(joblib_prediction)
    assert mlflow_prediction > 0
    assert joblib_prediction > 0