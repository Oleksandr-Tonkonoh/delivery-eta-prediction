from unittest.mock import Mock
import pytest
from genai import eta_explainer

def test_explain_delivery_eta_success(monkeypatch):
    delivery_data = {
        "distance_km": 5.2,
        "items_count": 3,
        "weather": "rain",
        "traffic_level": "high",
    }

    expected_eta = 57.479
    expected_explanation = "The predicted ETA is 57.48 minutes."

    prediction_mock = Mock(return_value=expected_eta)
    explanation_mock = Mock(return_value=expected_explanation)

    monkeypatch.setattr(eta_explainer, "predict_delivery_minutes", prediction_mock)
    monkeypatch.setattr(eta_explainer, "generate_explanation_response", explanation_mock)

    result = eta_explainer.explain_delivery_eta(delivery_data)

    assert result["predicted_delivery_minutes"] == expected_eta
    assert result["explanation"] == expected_explanation

    prediction_mock.assert_called_once_with(delivery_data)
    explanation_mock.assert_called_once()

    llm_input = explanation_mock.call_args.kwargs["input"]

    assert "Predicted ETA: 57.48 minutes." in llm_input
    assert "distance_km: 5.2" in llm_input
    assert "traffic_level: high" in llm_input


def test_eta_is_not_changed_by_llm(monkeypatch):
    delivery_data = {
        "distance_km": 5.2,
        "items_count": 3,
        "weather": "rain",
        "traffic_level": "high",
    }

    expected_eta =  57.479

    prediction_mock = Mock(return_value=expected_eta)
    explanation_mock = Mock(return_value="The ETA is 10 minutes.")

    monkeypatch.setattr(eta_explainer, "predict_delivery_minutes", prediction_mock)
    monkeypatch.setattr(eta_explainer, "generate_explanation_response", explanation_mock)

    result = eta_explainer.explain_delivery_eta(delivery_data)

    assert result["predicted_delivery_minutes"] == expected_eta
    assert result["explanation"] == "The ETA is 10 minutes."


def test_llm_error_propagates(monkeypatch):
    delivery_data = {
        "distance_km": 5.2,
        "items_count": 3,
        "weather": "rain",
        "traffic_level": "high",
    }
    
    expected_eta =  57.479
    
    prediction_mock = Mock(return_value=expected_eta)

    monkeypatch.setattr(eta_explainer, "predict_delivery_minutes", prediction_mock)
    monkeypatch.setattr(eta_explainer, 
                        "generate_explanation_response", 
                        Mock(side_effect=RuntimeError("LLM unavailable")))

    with pytest.raises(RuntimeError, match="LLM unavailable"):
        eta_explainer.explain_delivery_eta(delivery_data)
