from unittest.mock import Mock
from genai import llm_client
import pytest


@pytest.mark.parametrize(
    ("function_name", "prompt_uri"),
    [
        ("generate_explanation_response", "prompts:/explanation/1"),
        ("generate_RAG_response", "prompts:/RAG/2")
    ]
)


def test_generate_response_success(monkeypatch, function_name, prompt_uri):
    user_input = "Predicted ETA: 57.48 minutes."
    formatted_prompt = "Formatted prompt for Gemini"
    expected_response = "The delivery ETA is 57.48 minutes."

    prompt_mock = Mock()
    prompt_mock.format.return_value = formatted_prompt

    response_mock = Mock()
    response_mock.text = expected_response

    load_prompt_mock = Mock(return_value=prompt_mock)
    generate_content_mock = Mock(return_value=response_mock)

    monkeypatch.setattr(llm_client.mlflow.genai,
                        "load_prompt",
                        load_prompt_mock)

    monkeypatch.setattr(llm_client.client.models,
                        "generate_content",
                        generate_content_mock)

    function = getattr(llm_client, function_name)

    result = function(input=user_input)

    assert result == expected_response

    load_prompt_mock.assert_called_once_with(prompt_uri)
    prompt_mock.format.assert_called_once_with(input=user_input)
    generate_content_mock.assert_called_once_with(
        model=llm_client.model,
        contents=formatted_prompt
    )


def test_empty_llm_response_raises_error(monkeypatch):
    prompt_mock = Mock()
    prompt_mock.format.return_value = "Formatted prompt"

    response_mock = Mock()
    response_mock.text = ""

    load_prompt_mock = Mock(return_value=prompt_mock)
    generate_content_mock = Mock(return_value=response_mock)

    monkeypatch.setattr(
        llm_client.mlflow.genai,
        "load_prompt",
        load_prompt_mock
    )

    monkeypatch.setattr(
        llm_client.client.models,
        "generate_content",
        generate_content_mock
    )

    with pytest.raises(llm_client.LLMEmptyResponseError, 
                       match="The LLM returned an empty text response"):
        llm_client.generate_explanation_response(input="Test input")


def test_prompt_loading_error_is_wrapped(monkeypatch):
    monkeypatch.setattr(
        llm_client.mlflow.genai,
        "load_prompt",
        Mock(side_effect=RuntimeError("Prompt Registry unavailable"))
    ) 

    with pytest.raises(llm_client.LLMClientError, match="LLM request failed"):
        llm_client.generate_explanation_response(input="Test input")
                                                

def test_gemini_error_is_wrapped(monkeypatch):
    prompt_mock = Mock()
    prompt_mock.format.return_value = "Formatted prompt"
    
    response_mock = Mock()
    response_mock.text = ""
    
    load_prompt_mock = Mock(return_value=prompt_mock)
    
    monkeypatch.setattr(
        llm_client.mlflow.genai,
        "load_prompt",
        load_prompt_mock
    )
    
    monkeypatch.setattr(
        llm_client.client.models,
        "generate_content",
        Mock(side_effect=RuntimeError("Gemini unavailable"))
    )

    with pytest.raises(llm_client.LLMClientError, match="LLM request failed"):
        llm_client.generate_explanation_response(input="Test input")
