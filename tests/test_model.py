from api.model import predict_delivery_minutes

def test_prediction(delivery):

    predicted_delivery_minutes = predict_delivery_minutes(delivery)

    assert isinstance(predicted_delivery_minutes, float)
    assert predicted_delivery_minutes > 0