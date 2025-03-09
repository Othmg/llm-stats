"""
FastAPI NumPy Calculation Server

This server provides an API endpoint to perform numerical calculations using NumPy functions.
LLM assistants can send a POST request to the /calculate endpoint with a calculation name and data,
and the server will return the result of the calculation.

Allowed functions include:
- sum, mean, std, min, max, median, prod, var, cumsum, cumprod, diff, abs, sqrt, log, log10, exp, floor, ceil, round,
  sin, cos, tan, arcsin, arccos, arctan, square.

Endpoints:
- POST /calculate: Perform the specified calculation on provided data.
- GET /: Returns a welcome message.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any, Literal
from services.numpy_llm import CalculatorService
from services.scipy_llm import StatisticsService

app = FastAPI()


class CalculationRequest(BaseModel):
    service: Literal["calculator", "statistics"]
    calculation: str
    data: List[Any]


@app.post("/calculate")
def calculate(request: CalculationRequest):
    """
    Perform a numerical calculation based on the provided request.
    """
    try:
        service = {
            "calculator": CalculatorService,
            "statistics": StatisticsService,
        }.get(request.service)

        if not service:
            raise ValueError(f"Service '{request.service}' is not supported")

        result = service.perform_calculation(request.calculation, request.data)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    """
    Root endpoint of the API.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the FastAPI NumPy calculation server!"}
