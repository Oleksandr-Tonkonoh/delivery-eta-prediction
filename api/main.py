from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .schemas import Delivery, DeliveryMinutesResponse, ExplanationResponse, AskRequest, SourceReference, AskResponse
from .model import predict_delivery_minutes
from genai.eta_explainer import explain_delivery_eta
from genai.rag_service import answer_delivery_question
from genai.llm_client import LLMClientError
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
                                       exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": error["loc"][-1],
            "message": error["msg"]
        }) 
    
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation failed",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request,
                                    exc: Exception):
    logger.exception("Unhandled error: %s %s",
                     request.method,
                     request.url)

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=DeliveryMinutesResponse)
def prediction(delivery: Delivery):
    delivery_data = delivery.model_dump()

    predicted_delivery_minutes = predict_delivery_minutes(delivery_data)

    return {"predicted_delivery_minutes": predicted_delivery_minutes}


@app.post("/explain", response_model=ExplanationResponse)
def eta_explanation(delivery: Delivery):
    delivery_data = delivery.model_dump()

    result = explain_delivery_eta(delivery_data)

    return {
        "predicted_delivery_minutes": result["predicted_delivery_minutes"],
        "explanation": result["explanation"]
    }


@app.post("/ask", response_model=AskResponse)
def ask_delivery_question(request: AskRequest):
    try:
        result = answer_delivery_question(request.question)
        return result
    
    except LLMClientError as err:
        raise HTTPException(
            status_code=502,
            detail="The delivery assistant is temporarily unavailable"
        ) from err