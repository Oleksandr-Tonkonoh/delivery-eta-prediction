from typing import Any
from api.model import predict_delivery_minutes
from .llm_client import generate_explanation_response

def explain_delivery_eta(delivery_data: dict) -> dict:
    predicted_delivery_minutes = predict_delivery_minutes(delivery_data)

    indicators = "\n".join(
        f"- {name}: {value}"
        for name, value in delivery_data.items()
    )

    llm_input = (
        f"Predicted ETA: {predicted_delivery_minutes:.2f} minutes.\n\n"
        f"Delivery indicators:\n{indicators}"
    )
    
    explanation = generate_explanation_response(input=llm_input)

    return {
        "predicted_delivery_minutes": float(predicted_delivery_minutes),
        "explanation": explanation
    }

