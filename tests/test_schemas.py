import pytest
from api.schemas import Delivery
from pydantic import ValidationError


def test_valid_delivery(delivery):
    delivery_test = Delivery(**delivery)

    assert delivery_test.traffic_level == delivery["traffic_level"]
    assert delivery_test.restaurant_rating == delivery["restaurant_rating"]


def test_invalid_restaurant_rating(delivery):
    delivery["restaurant_rating"] = - 1

    with pytest.raises(ValidationError):
        Delivery(**delivery)
