# Delivery ETA Prediction API

A machine learning project for predicting delivery time, serving predictions through a REST API, explaining model outputs with a Large Language Model (LLM), and answering delivery-related questions using Retrieval-Augmented Generation (RAG).

The project combines machine learning, data engineering, API development, experiment tracking, and generative AI in a single application.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [MLflow Integration](#mlflow-integration)
- [Generative AI Integration](#generative-ai-integration)
- [RAG Pipeline](#rag-pipeline)
- [API Endpoints](#api-endpoints)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Local Setup](#local-setup)
- [Running with Docker](#running-with-docker)
- [Testing](#testing)
- [SQL and Data Processing](#sql-and-data-processing)
- [Visualizations](#visualizations)
- [Security and Data Management](#security-and-data-management)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [License](#license)

## Overview

Delivery time estimation is an important problem in delivery services. Accurate predictions help customers understand when an order is likely to arrive and help delivery platforms manage expectations.

This project uses a trained machine learning model to estimate delivery duration. The model is exposed through a FastAPI application, while MLflow is used to load a registered model and manage model-related assets.

The application also integrates generative AI in two ways:

1. **ETA explanation:** generates a natural-language explanation of a model prediction.
2. **Delivery question answering:** retrieves relevant information from a local knowledge base and uses an LLM to formulate an answer.

The machine learning model remains responsible for the numerical ETA prediction. The LLM provides explanations and answers questions; it does not replace the predictive model.

## Key Features

- Delivery time prediction using a trained machine learning model.
- REST API built with FastAPI.
- Interactive API documentation through Swagger UI.
- Model loading through the MLflow Model Registry.
- LLM-based explanations of delivery predictions.
- Retrieval-Augmented Generation (RAG) over delivery-related documents.
- TF-IDF-based document retrieval.
- Prompt management through MLflow.
- Data preparation and analysis using SQL.
- Automated tests with pytest.
- Docker images for the API and MLflow server.
- GitHub Actions workflow for automated testing and Docker image builds.

## Architecture

The application consists of several components:

- **Data layer:** raw and processed delivery datasets.
- **Machine learning layer:** trained model used to predict delivery duration.
- **API layer:** FastAPI endpoints that expose prediction and generative AI functionality.
- **MLflow layer:** model registry, experiment tracking, artifacts, and prompt management.
- **Generative AI layer:** LLM client and ETA explanation service.
- **Retrieval layer:** document processing, TF-IDF retrieval, and RAG response generation.
- **Knowledge base:** Markdown documents containing delivery policies and FAQs.
- **Testing layer:** automated tests for the API, model, schemas, MLflow integration, and RAG functionality.

### Request Flow

For an ETA prediction:

1. A client sends delivery features to the API.
2. FastAPI validates the request.
3. The registered machine learning model predicts the delivery duration.
4. The API returns the numerical prediction.

For an ETA explanation:

1. The API obtains the model prediction.
2. The explanation service prepares the prediction and relevant context.
3. The LLM generates a natural-language explanation.
4. The API returns the explanation without allowing the LLM to change the numerical prediction.

For a delivery-related question:

1. The client submits a question.
2. The retriever searches the local knowledge base.
3. Relevant document content is added to the prompt.
4. The LLM generates an answer using the retrieved context.
5. The API returns the response.

## Technology Stack

### Programming Language

- Python 3.13

### Machine Learning and Data Processing

- pandas
- NumPy
- scikit-learn
- SQL
- pickle-based model files

### API Development

- FastAPI
- Uvicorn
- Pydantic

### Model Management

- MLflow
- MLflow Model Registry
- MLflow prompt management

### Generative AI

- Google Gemini API
- TF-IDF retrieval
- Retrieval-Augmented Generation (RAG)

### Development and Deployment

- pytest
- Docker
- Docker Compose
- Git
- GitHub Actions
- GitHub Container Registry (GHCR), if image publishing is enabled

## Project Structure

```text
delivery_eta_project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── model.py
│   └── schemas.py
├── data/
│   ├── raw/
│   │   ├── couriers.csv
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   ├── restaurants.csv
│   │   └── weather_daily.csv
│   └── processed/
│       └── final_ml_dataset.csv
├── genai/
│   ├── __init__.py
│   ├── config.py
│   ├── eta_explainer.py
│   ├── ingest.py
│   ├── llm_client.py
│   ├── prompts.py
│   ├── rag_service.py
│   ├── register_prompts.py
│   ├── register_rag_prompt.py
│   └── retriever.py
├── images/
│   ├── actual_vs_predicted.png
│   └── residuals.png
├── knowledge/
│   ├── cancellation_policy.md
│   ├── courier_faq.md
│   ├── delivery_policy.md
│   ├── index.json
│   └── weather_delivery_guidelines.md
├── mlflow_tracking/
│   ├── __init__.py
│   ├── main.py
│   ├── model_utils.py
│   ├── verify_registered_model.py
│   ├── dataset_info.txt
│   └── feature_names.txt
├── models/
│   ├── ElasticNet.pkl
│   ├── final_model.pkl
│   ├── HistGradientBoosting-default.pkl
│   ├── Lasso.pkl
│   ├── LinearRegression.pkl
│   └── Ridge.pkl
├── notebooks/
│   ├── delivery_eta_prediction.ipynb
│   └── Untitled.ipynb
├── sql/
│   ├── create_tables.sql
│   ├── 01_data_quality.sql
│   ├── 02_referential_integrity.sql
│   ├── 03_basic_analysis.sql
│   ├── 04_time_analysis.sql
│   ├── 05_delivery_datamart.sql
│   ├── 06_historical_features.sql
│   ├── 07_weather_features.sql
│   └── 08_final_ml_dataset.sql
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_genai.py
│   ├── test_llm_client.py
│   ├── test_mlflow.py
│   ├── test_model.py
│   ├── test_rag.py
│   ├── test_rag_service.py
│   └── test_schemas.py
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.mlflow
├── requirements.txt
├── README.md
└── test_retriever_manual.py
```

**Note:** Local configuration files, caches, and generated MLflow databases or artifacts are not included in this overview. The `.env` file must not be committed to the repository.

## Machine Learning Pipeline

The project includes data preparation, model training, evaluation, and model management components.

### Data Sources

The repository contains datasets related to:

- Orders
- Customers
- Couriers
- Restaurants
- Daily weather information

The processed dataset used by the project is stored in `data/processed/final_ml_dataset.csv`.

### Model Training and Evaluation

The `notebooks/delivery_eta_prediction.ipynb` notebook contains the model development workflow.

The repository includes saved models for several regression algorithms:

- Linear Regression
- Ridge Regression
- Lasso Regression
- ElasticNet
- HistGradientBoosting

The selected model is used for delivery duration prediction. Model quality should be evaluated on data that was not used for training.

Useful regression metrics include:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Coefficient of determination (\(R^2\))

The actual model performance should be reported using the measured evaluation results rather than assumed values.

## MLflow Integration

MLflow is used to manage the machine learning model and related artifacts.

The project includes:

- Model registration and verification utilities.
- Model loading from the MLflow Model Registry.
- A dedicated MLflow server configuration.
- Prompt registration utilities for generative AI functionality.

The API is configured to load the registered model using a model URI such as:

```text
models:/delivery-eta-model/3
```

The model name and version must exist in the configured MLflow registry.

### MLflow UI

When the MLflow server is running locally, its web interface is available at:

```text
http://localhost:5000
```

The interface can be used to inspect registered models, runs, and available artifacts.

**Important:** the MLflow tracking database and artifact storage must remain available between restarts. For Docker deployments, use persistent storage rather than relying on data inside a temporary container filesystem.

## Generative AI Integration

The `genai/` package contains the code responsible for LLM integration and AI-powered application functionality.

Important modules include:

- `config.py` — loads configuration and environment variables.
- `llm_client.py` — provides the LLM client and response-generation functionality.
- `eta_explainer.py` — prepares explanations of ETA predictions.
- `prompts.py` — contains prompt-related functionality.
- `register_prompts.py` — registers explanation prompts with MLflow.
- `register_rag_prompt.py` — registers the RAG prompt with MLflow.

### ETA Explanations

The explanation service uses the predicted delivery duration and relevant context to generate a readable explanation.

The purpose is to make the model's output easier to understand, not to produce a second ETA estimate.

LLM-generated explanations may be incomplete or inaccurate. They should not be interpreted as a formal explanation of the model's internal decision process unless a separate model-explanation method is implemented and validated.

## RAG Pipeline

Retrieval-Augmented Generation combines document retrieval with LLM-based response generation.

The project's knowledge base contains Markdown documents about delivery policies, courier FAQs, cancellations, and weather-related delivery guidance.

### Knowledge Base

The `knowledge/` directory contains:

- `delivery_policy.md`
- `cancellation_policy.md`
- `courier_faq.md`
- `weather_delivery_guidelines.md`
- `index.json`

### Retrieval Process

The RAG workflow consists of the following stages:

1. Load and process the knowledge documents.
2. Prepare the searchable document representation.
3. Retrieve relevant content for a user's question using TF-IDF-based retrieval.
4. Insert the retrieved content into the prompt.
5. Ask the LLM to generate a response using that context.

Relevant code is located in:

- `genai/ingest.py`
- `genai/retriever.py`
- `genai/rag_service.py`
- `genai/llm_client.py`

The quality of a RAG answer depends on the relevance of the retrieved documents and the quality of the generated response. The system should not be assumed to answer correctly when the knowledge base does not contain the requested information.

## API Endpoints

The FastAPI application is implemented in `api/main.py`.

The project provides the following main endpoint functionality.

### `GET /docs`

Opens the interactive Swagger UI documentation.

```text
http://localhost:8000/docs
```

### `POST /predict`

Predicts delivery duration using the registered machine learning model.

The request must contain the delivery features required by the application's Pydantic request schema.

Example request structure — replace the placeholder with the actual fields required by `api/schemas.py`:

```json
{
  "feature_1": 1,
  "feature_2": 2
}
```

### `POST /explain`

Generates a natural-language explanation of a delivery ETA prediction.

This endpoint requires the prediction input and an operational LLM configuration.

### `POST /ask`

Answers a delivery-related question using the RAG pipeline.

Example request structure — confirm the exact field name in `api/schemas.py`:

```json
{
  "question": "What happens if my delivery is delayed?"
}
```

The exact request and response fields should be taken from the current API schemas and endpoint implementation.

## Requirements

Before running the project, install:

- Python 3.13
- Git
- Docker Desktop, if using Docker
- A Google Gemini API key, if using the Gemini provider
- Access to the required registered model and prompts in MLflow

Install Python dependencies from `requirements.txt`.

## Configuration

The application uses environment variables for service configuration.

Create a local `.env` file in the project root if it does not already exist.

Example:

```dotenv
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.8-flash
LLM_API_KEY=your_gemini_api_key
LLM_TIMEOUT_SECONDS=30
MLFLOW_TRACKING_URI=http://localhost:5000
```

Replace `your_gemini_api_key` with your actual API key.

The model name shown above is an example based on the project configuration; use a model currently available to your Gemini API account.

### Local vs Docker Configuration

When running the API directly on your computer, the MLflow URI generally points to:

```text
http://localhost:5000
```

When running the API inside Docker Compose, the API container should use the MLflow service name:

```text
http://mlflow:5000
```

Inside a container, `localhost` refers to that container itself, not another container.

**Security:** never commit `.env` or expose API keys in source code, README examples, logs, or GitHub Actions output.

## Local Setup

### 1. Clone the Repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd delivery_eta_project
```

Replace the placeholder with the actual repository URL.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
py -3.13 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use the activation method permitted by your system policy or run the commands through a terminal that supports the environment activation.

### 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` in the project root and set the variables described in the [Configuration](#configuration) section.

### 5. Start MLflow

If the registered model and prompts are stored in your local MLflow instance, start the MLflow server using the project's existing configuration.

For example, if your MLflow backend is configured for SQLite:

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

This basic command is suitable only when it matches the backend and artifact configuration used by the project. If your model registry uses a specific backend store or artifact location, start MLflow with those same settings.

### 6. Verify the Registered Model

Check that the registered model exists and that the expected version can be accessed.

The repository includes:

```text
mlflow_tracking/verify_registered_model.py
```

Run it according to its command-line interface and configuration.

### 7. Start the API

From the project root:

```powershell
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

You can now inspect the available endpoints and submit requests through Swagger UI.

## Running with Docker

Docker Compose can run the API and MLflow as separate services.

### 1. Check Docker

Make sure Docker Desktop is running, then execute:

```powershell
docker --version
docker compose version
```

### 2. Check Configuration

Ensure that:

- `.env` exists and contains the required configuration.
- The API image includes the application packages and knowledge documents it needs.
- The API uses `http://mlflow:5000` to connect to MLflow inside Compose.
- MLflow's backend database and artifacts are stored persistently.
- The registered model and required prompts are available to the running MLflow instance.

### 3. Build and Start Services

From the project root:

```powershell
docker compose up --build -d
```

Check the running containers:

```powershell
docker compose ps
```

Inspect the API logs:

```powershell
docker compose logs -f api
```

Inspect the MLflow logs:

```powershell
docker compose logs -f mlflow
```

### 4. Open the Services

API documentation:

```text
http://localhost:8000/docs
```

MLflow UI:

```text
http://localhost:5000
```

### 5. Stop the Services

```powershell
docker compose down
```

To preserve named volumes, do not add `-v`.

**Important:** starting containers does not automatically register a model or make an existing model registry available. The MLflow backend, artifacts, registered model version, and prompt resources must be configured correctly.

## Testing

The project includes a pytest test suite in `tests/`.

Test files cover areas such as:

- API endpoints
- Request and response schemas
- Model functionality
- MLflow integration
- LLM client behavior
- Generative AI functionality
- RAG service and retrieval

### Run the Tests

Activate the virtual environment and execute:

```powershell
python -m pytest -v
```

### Manual Retriever Test

The repository also contains:

```text
test_retriever_manual.py
```

Use it to inspect the retriever's behavior according to the script's implementation.

## SQL and Data Processing

The `sql/` directory contains SQL scripts for data preparation and analysis.

The scripts cover:

- Table creation
- Data quality checks
- Referential integrity
- Basic analytical queries
- Time-based analysis
- Delivery data mart preparation
- Historical features
- Weather features
- Final machine learning dataset preparation

The final processed dataset is located at:

```text
data/processed/final_ml_dataset.csv
```

The raw source files are stored under `data/raw/`.

The exact database engine, schema, and execution order should be confirmed from the SQL scripts and the project's data preparation workflow.

## Visualizations

The `images/` directory contains model evaluation visualizations:

- `actual_vs_predicted.png` — compares actual delivery durations with model predictions.
- `residuals.png` — visualizes prediction residuals.

These plots can help identify systematic prediction errors and assess how closely predictions match observed values.

