import joblib
from pathlib import Path
import pandas as pd
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error


BASE_DIR = Path(__file__).parent.parent

final_model = joblib.load(BASE_DIR / "models" / "final_model.pkl")
lr = joblib.load(BASE_DIR / "models" / "LinearRegression.pkl")
Rg = joblib.load(BASE_DIR / "models" / "Ridge.pkl")
Lo = joblib.load(BASE_DIR / "models" / "Lasso.pkl")
EN = joblib.load(BASE_DIR / "models" / "ElasticNet.pkl")
hgbr = joblib.load(BASE_DIR / "models" / "HistGradientBoosting-default.pkl")

df = pd.read_csv(BASE_DIR / "data" / "processed" / "final_ml_dataset.csv")


# Time Based Split
n = len(df)
train_end = int(n * 0.70)
val_end = int(n * 0.85)

train_df = df.iloc[:train_end]
val_df = df.iloc[train_end:val_end]
test_df = df.iloc[val_end:]

X_train = train_df.drop(columns=["order_id", "restaurant_id", "courier_id", "delivery_minutes", "order_ts", "date"]) 
y_train = train_df["delivery_minutes"]

X_val = val_df.drop(columns=["order_id", "restaurant_id", "courier_id", "delivery_minutes", "order_ts", "date"])
y_val = val_df["delivery_minutes"]

X_test = test_df.drop(columns=["order_id", "restaurant_id", "courier_id", "delivery_minutes", "order_ts", "date"])
y_test = test_df["delivery_minutes"]


input_example = X_train.iloc[[0]]
prediction = final_model.predict(input_example)[0]


# Calculate Final model Metrics
final_test_preds = final_model.predict(X_test)
final_val_preds = final_model.predict(X_val)

final_test_RMSE = root_mean_squared_error(y_test,final_test_preds)
final_test_MAE = mean_absolute_error(y_test, final_test_preds)
final_test_r2 = r2_score(y_test, final_test_preds)
final_test_MAPE = mean_absolute_percentage_error(y_test, final_test_preds) * 100

final_val_RMSE = root_mean_squared_error(y_val, final_val_preds)
final_val_MAE = mean_absolute_error(y_val, final_val_preds)
final_val_r2 = r2_score(y_val, final_val_preds)
final_val_MAPE = mean_absolute_percentage_error(y_val, final_val_preds) * 100


# Calculate Linear Regression Metrics
lr_preds = lr.predict(X_val)

lr_RMSE = root_mean_squared_error(y_val, lr_preds)
lr_MAE = mean_absolute_error(y_val, lr_preds)
lr_r2 = r2_score(y_val, lr_preds)
lr_MAPE = mean_absolute_percentage_error(y_val, lr_preds) * 100


# Calculate Ridge Metrics
Rg_preds = Rg.predict(X_val)

Rg_RMSE = root_mean_squared_error(y_val, Rg_preds)
Rg_MAE = mean_absolute_error(y_val, Rg_preds)
Rg_r2 = r2_score(y_val, Rg_preds)
Rg_MAPE = mean_absolute_percentage_error(y_val, Rg_preds) * 100


# Calculate Lasso Metrics
Lo_preds = Lo.predict(X_val)

Lo_RMSE = root_mean_squared_error(y_val, Lo_preds)
Lo_MAE = mean_absolute_error(y_val, Lo_preds)
Lo_r2 = r2_score(y_val, Lo_preds)
Lo_MAPE = mean_absolute_percentage_error(y_val, Lo_preds) * 100


# Calculate ElasticNet Metrics
EN_preds = EN.predict(X_val)

EN_RMSE = root_mean_squared_error(y_val, EN_preds)
EN_MAE = mean_absolute_error(y_val, EN_preds)
EN_r2 = r2_score(y_val, EN_preds)
EN_MAPE = mean_absolute_percentage_error(y_val, EN_preds) * 100


# Calculate HistGradientBoosting-default metrics
hgbr_preds = hgbr.predict(X_val)

hgbr_RMSE = root_mean_squared_error(y_val, hgbr_preds)
hgbr_MAE = mean_absolute_error(y_val, hgbr_preds)
hgbr_r2 = r2_score(y_val, hgbr_preds)
hgbr_MAPE = mean_absolute_percentage_error(y_val, hgbr_preds) * 100


# Define df params
df_params = {
    "df_length": len(df),
    "train_rows_length": len(train_df),
    "validation_rows_length": len(val_df),
    "test_rows_length": len(test_df),
    "train_ratio": len(train_df) / len(df),
    "validation_ratio": len(val_df) / len(df),
    "test_ratio": len(test_df) / len(df)
}