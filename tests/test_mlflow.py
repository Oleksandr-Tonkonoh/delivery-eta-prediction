import pandas as pd


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

    assert mlflow_prediction == joblib_prediction
    assert mlflow_prediction > 0 and joblib_prediction > 0



    