import mlflow
from mlflow.models import infer_signature
from model_utils import (
    BASE_DIR,
    final_model, 
    df_params, 
    input_example,
    prediction,
    final_test_RMSE, 
    final_test_MAE, 
    final_test_r2, 
    final_test_MAPE,
    final_val_RMSE,
    final_val_MAE,
    final_val_r2,
    final_val_MAPE,
    lr,
    lr_RMSE,
    lr_MAE,
    lr_r2, 
    lr_MAPE,
    Rg,
    Rg_RMSE,
    Rg_MAE,
    Rg_r2,
    Rg_MAPE,
    Lo,
    Lo_RMSE,
    Lo_MAE, 
    Lo_r2,
    Lo_MAPE, 
    EN, 
    EN_RMSE,
    EN_MAE, 
    EN_r2,
    EN_MAPE,
    hgbr,
    hgbr_RMSE,
    hgbr_MAE, 
    hgbr_r2,
    hgbr_MAPE
)

mlflow.set_tracking_uri("http://localhost:5000")

mlflow.set_experiment(experiment_name="delivery-eta-prediction-docker")

signature = infer_signature(
    input_example,
    prediction
)

with mlflow.start_run(run_name="HistGradientBoosting-tuned(Final model)"):
    model_params = final_model.named_steps["model"].get_params()

    metrics = {
        "test_RMSE": final_test_RMSE,
        "test_MAE": final_test_MAE,
        "test_R2": final_test_r2,
        "test_MAPE": final_test_MAPE,

        "val_RMSE": final_val_RMSE,
        "val_MAE": final_val_MAE,
        "val_R2": final_val_r2,
        "val_MAPE": final_val_MAPE
    }

    # log params
    mlflow.log_params(df_params)
    mlflow.log_params(model_params)

    #log metrics
    mlflow.log_metrics(metrics)

    #log model
    mlflow.sklearn.log_model(sk_model=final_model, 
                             name="Final model", 
                             registered_model_name="delivery-eta-model",
                             serialization_format="cloudpickle",
                             signature=signature,
                             input_example=input_example)

    #log artifacts
    mlflow.log_artifact(str(BASE_DIR / "mlflow_tracking" / "dataset_info.txt"))
    mlflow.log_artifact(str(BASE_DIR /"mlflow_tracking" / "feature_names.txt"))
    mlflow.log_artifact(str(BASE_DIR / "images" / "residuals.png"))
    mlflow.log_artifact(str(BASE_DIR / "images" / "actual_vs_predicted.png"))


with mlflow.start_run(run_name="LinearRegression"):
    model_params = lr.named_steps["model"].get_params()

    metrics = {
        "val_RMSE": lr_RMSE,
        "val_MAE": lr_MAE,
        "val_R2": lr_r2,
        "val_MAPE": lr_MAPE
    }

    # log params
    mlflow.log_params(df_params)
    mlflow.log_params(model_params)

    #log metrics
    mlflow.log_metrics(metrics)

    #log model
    mlflow.sklearn.log_model(sk_model=lr, name="LinearRegression", serialization_format="cloudpickle")


with mlflow.start_run(run_name="Ridge"):
    model_params = Rg.named_steps["model"].get_params()

    metrics = {
        "val_RMSE": Rg_RMSE,
        "val_MAE": Rg_MAE,
        "val_R2": Rg_r2,
        "val_MAPE": Rg_MAPE
    }

    # log params
    mlflow.log_params(df_params)
    mlflow.log_params(model_params)

    #log metrics
    mlflow.log_metrics(metrics)

    #log model
    mlflow.sklearn.log_model(sk_model=Rg, name="Ridge", serialization_format="cloudpickle")


with mlflow.start_run(run_name="Lasso"):
    model_params = Lo.named_steps["model"].get_params()

    metrics = {
        "val_RMSE": Lo_RMSE,
        "val_MAE": Lo_MAE,
        "val_R2": Lo_r2,
        "val_MAPE": Lo_MAPE
    }

    # log params
    mlflow.log_params(df_params)
    mlflow.log_params(model_params)

    #log metrics
    mlflow.log_metrics(metrics)

    #log model
    mlflow.sklearn.log_model(sk_model=Lo, name="Lasso", serialization_format="cloudpickle")


with mlflow.start_run(run_name="ElasticNet"):
    model_params = EN.named_steps["model"].get_params()

    metrics = {
        "val_RMSE": EN_RMSE,
        "val_MAE": EN_MAE,
        "val_R2": EN_r2,
        "val_MAPE": EN_MAPE
    }

    # log params
    mlflow.log_params(df_params)
    mlflow.log_params(model_params)

    #log metrics
    mlflow.log_metrics(metrics)

    #log model
    mlflow.sklearn.log_model(sk_model=EN, name="ElasticNet", serialization_format="cloudpickle")


with mlflow.start_run(run_name="HistGradientBoosting-default"):
    model_params = hgbr.named_steps["model"].get_params()

    metrics = {
        "val_RMSE": hgbr_RMSE,
        "val_MAE": hgbr_MAE,
        "val_R2": hgbr_r2,
        "val_MAPE": hgbr_MAPE
    }

    # log params
    mlflow.log_params(df_params)
    mlflow.log_params(model_params)

    #log metrics
    mlflow.log_metrics(metrics)

    #log model
    mlflow.sklearn.log_model(sk_model=hgbr, name="HistGradientBoosting-default", serialization_format="cloudpickle")