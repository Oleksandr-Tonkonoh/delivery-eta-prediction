import mlflow
from .config import mlflow_tracking_uri
from .prompts import explanation_prompt, rag_prompt

def register_prompts() -> None: 
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name="delivery-eta-prediction") 
    
    mlflow.genai.register_prompt( 
        name="explanation", 
        template=explanation_prompt, 
        commit_message="Initial explanation prompt" 
    ) 

    mlflow.genai.register_prompt( 
        name="RAG", 
        template=rag_prompt, 
        commit_message="Initial RAG prompt"
    ) 
    
if __name__ == "__main__": 
    register_prompts()