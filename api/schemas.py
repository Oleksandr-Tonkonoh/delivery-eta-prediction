from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Delivery(BaseModel):
    distance_km: float = Field(ge=0)
    items_count: int = Field(gt=0)
    order_amount: float = Field(ge=0)
    weather: Literal["cloudy", "rain", "snow", "clear"]
    traffic_level: Literal["low", "medium", "high"]
    avg_prep_minutes: float = Field(ge=0)
    restaurant_rating: float = Field(ge=0, le=5)
    vehicle: Literal["bike", "car", "scooter"]
    courier_rating: float = Field(ge=0, le=5)
    experience_months: int = Field(ge=0)
    order_hour: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)
    is_weekend: bool
    restaurant_previous_orders_count: int = Field(ge=0)
    restaurant_historical_avg_delivery: float | None = None
    courier_previous_orders_count: int = Field(ge=0)
    courier_historical_avg_delivery: float | None = None
    avg_temp_c: float
    rain_mm: float = Field(ge=0)
    snow_cm: float = Field(ge=0)
    hour_sin: float
    hour_cos: float
    day_of_week_sin: float
    day_of_week_cos: float
    is_peak_hour: bool
    month: int = Field(ge=1, le=12)

    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }


class DeliveryMinutesResponse(BaseModel):
    predicted_delivery_minutes: float


class ExplanationResponse(BaseModel):
    predicted_delivery_minutes: float
    explanation: str


class AskRequest(BaseModel):
    question: str = Field(min_length=1)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question must not be empty")

        return value


class SourceReference(BaseModel):
    source: str
    chunk_id: str
    score: float = Field(ge=0, le=1)


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceReference]