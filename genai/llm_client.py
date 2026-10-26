import mlflow
from google import genai
from google.genai import types
from .config import llm_api_key, model, timeout, mlflow_tracking_uri


class LLMClientError(RuntimeError):
     pass
class LLMEmptyResponseError(LLMClientError):
     pass


mlflow.set_tracking_uri(mlflow_tracking_uri)

client = genai.Client(
    api_key=llm_api_key,
    http_options=types.HttpOptions(timeout=int(timeout * 1000))    
)


explanation_prompt_uri = "prompts:/explanation/1"
rag_prompt_uri = "prompts:/RAG/2"


def generate_explanation_response(input:str) -> str:
    try:
        prompt = mlflow.genai.load_prompt(explanation_prompt_uri)
        message = prompt.format(input=input)
        response = client.models.generate_content(
            model=model,
            contents=message
        )
    except Exception as e:
        raise LLMClientError("LLM request failed") from e

    if not response.text or not response.text.strip():
        raise LLMEmptyResponseError("The LLM returned an empty text response")

    return response.text


def generate_RAG_response(input: str) -> str:
    try:
        prompt = mlflow.genai.load_prompt(rag_prompt_uri)
        message = prompt.format(input=input)
        response = client.models.generate_content(
            model=model,
            contents=message
        )
    except Exception as e:
            raise LLMClientError("LLM request failed") from e
    
    if not response.text or not response.text.strip():
        raise LLMEmptyResponseError("The LLM returned an empty text response")
    
    return response.text
