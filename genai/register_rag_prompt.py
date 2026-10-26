import mlflow
from dotenv import load_dotenv

from genai.config import mlflow_tracking_uri
from genai.prompts import rag_prompt


load_dotenv()

mlflow.set_tracking_uri(mlflow_tracking_uri)

registered_prompt = mlflow.genai.register_prompt(
    name="RAG",
    template=rag_prompt,
    commit_message="Remove duplicate Sources section from RAG answers",
)