def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_delivery_time(client, delivery):
    response = client.post("/predict",
                           json=delivery)

    delivery_data = response.json()

    assert response.status_code == 200
    assert "predicted_delivery_minutes" in delivery_data
    assert delivery_data["predicted_delivery_minutes"] > 0


def test_invalid_delivery(client, delivery):
    delivery["restaurant_rating"] = -1

    response = client.post("/predict",
                           json=delivery)

    assert response.status_code == 422

    delivery_data = response.json()

    assert delivery_data["message"] == "Validation failed"
    assert "errors" in delivery_data


def test_explain_delivery(client, delivery):
    response = client.post("/explain",
                           json=delivery)

    delivery_data = response.json()
    
    assert response.status_code == 200
    assert "predicted_delivery_minutes" in delivery_data
    assert delivery_data["predicted_delivery_minutes"] > 0
    assert "explanation" in delivery_data

