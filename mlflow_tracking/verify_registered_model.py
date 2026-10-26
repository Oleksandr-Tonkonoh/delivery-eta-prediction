import mlflow
from model_utils import X_test, y_test, final_model as joblib_model

mlflow.set_tracking_uri("http://localhost:5000")

mlflow.set_experiment(experiment_name="delivery-eta-prediction")


model_uri = "models:/delivery-eta-model/3"

mlflow_model = mlflow.pyfunc.load_model(model_uri)

test_row = X_test.iloc[[0]]

actual = y_test.iloc[0]

mlflow_pred = mlflow_model.predict(test_row)[0]
joblib_pred = joblib_model.predict(test_row)[0]

mlflow_error = abs(actual - mlflow_pred)
joblib_error = abs(actual - joblib_pred)

prediction_difference = abs(mlflow_pred - joblib_pred)


with mlflow.start_run(run_name="Registry verification"):
    params = {
        "model_uri": model_uri,
        "test_row_index": str(X_test.index[0])
    }

    metrics = {
        "Actual": actual,
        "MLflow prediction": mlflow_pred,
        "Joblib prediction": joblib_pred,
        "MLflow absolute error": round(mlflow_error, 2),
        "Joblib absolute error": round(joblib_error, 2),
        "Prediction difference": round(prediction_difference, 3)
    }

    mlflow.log_params(params)
    mlflow.log_metrics(metrics)
