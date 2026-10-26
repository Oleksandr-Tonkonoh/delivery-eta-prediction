import os
from dotenv import load_dotenv

load_dotenv()

# load environmental variables
provider=os.getenv("LLM_PROVIDER").strip().lower()
model=os.getenv("LLM_MODEL").strip()
llm_api_key = os.getenv("LLM_API_KEY").strip()
timeout=os.getenv("LLM_TIMEOUT_SECONDS", "30")
mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI","http://localhost:5000").strip()

# chech compulsory parameters
if not provider:
    raise ValueError("Provider is required")

if not model:
    raise ValueError("Model is required")

if not llm_api_key:
    raise ValueError("API key is required")


# convert a timeout to a numeric type
try:
    timeout = float(timeout)
except Exception as e:
    raise ValueError("timeout must be a number", e)


# check that a timeout is a positive number
if timeout <= 0:
    raise ValueError("timeout must be a positive number")

