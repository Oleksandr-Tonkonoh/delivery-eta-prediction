from fastapi.testclient import TestClient
import pytest
import mlflow
import joblib
from pathlib import Path
from api.main import app

@pytest.fixture
def client():

    return TestClient(app)


@pytest.fixture
def delivery():
    
    return {
        "distance_km": 5.2,
        "items_count": 3,
        "order_amount": 24.5,
        "weather": "rain",
        "traffic_level": "high",
        "avg_prep_minutes": 18.0,
        "restaurant_rating": 4.6,
        "vehicle": "car",
        "courier_rating": 4.2,
        "experience_months": 14,
        "order_hour": 18,
        "day_of_week": 2,
        "is_weekend": False,
        "restaurant_previous_orders_count": 125,
        "restaurant_historical_avg_delivery": 34.7,
        "courier_previous_orders_count": 230,
        "courier_historical_avg_delivery": 31.4,
        "avg_temp_c": 12.5,
        "rain_mm": 4.2,
        "snow_cm": 0.0,
        "hour_sin": -1.0,
        "hour_cos": 0.0,
        "day_of_week_sin": 0.97,
        "day_of_week_cos": -0.22,
        "is_peak_hour": True,
        "month": 5        
    }


@pytest.fixture
def mlflow_model():
    mlflow.set_tracking_uri("http://localhost:5000")

    return mlflow.pyfunc.load_model("models:/delivery-eta-model/3")


@pytest.fixture
def joblib_model():
    BASE_DIR = Path(__file__).resolve().parent.parent

    return joblib.load(BASE_DIR / "models" / "final_model.pkl")