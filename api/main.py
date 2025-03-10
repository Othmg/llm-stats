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

from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, validator
from typing import List, Any, Literal, Optional, Dict, Union
from api.services.numpy_llm import CalculatorService
from api.services.scipy_llm import StatisticsService
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog
import sys
from datetime import datetime
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import asyncio
from functools import partial
import resource

# Configure structlog to output to stdout
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "*.statsforllm.com",  # Your production domain
        "*.vercel.app",  # Vercel preview deployments
        "localhost",  # Local development
        "127.0.0.1",  # Local development
    ],
)


class CalculationRequest(BaseModel):
    service: Literal["calculator", "statistics"]
    calculation: str
    data: Union[List[Any], Dict[str, List[float]]]
    params: Optional[Dict[str, Any]] = {}

    @validator("data")
    def validate_data(cls, v):
        # First check the type
        if not isinstance(v, (list, dict)):
            raise ValueError("Data must be either a list or a dict of lists")

        # Handle list input
        if isinstance(v, list):
            if len(v) > 10000:
                raise ValueError("Data array too large")
            if not all(isinstance(x, (int, float)) for x in v):
                raise ValueError("All values must be numbers")
            if any(abs(float(x)) > 1e308 for x in v):
                raise ValueError("Numbers too large - must be within float64 range")

        # Handle dictionary input
        elif isinstance(v, dict):
            for key, value in v.items():
                if not isinstance(value, list):
                    raise ValueError(f"Value for key '{key}' must be a list")
                if len(value) > 10000:
                    raise ValueError(f"Data array too large for key '{key}'")
                if not all(isinstance(x, (int, float)) for x in value):
                    raise ValueError(f"All values in key '{key}' must be numbers")
                if any(abs(float(x)) > 1e308 for x in value):
                    raise ValueError(
                        f"Numbers in key '{key}' too large - must be within float64 range"
                    )

        return v


def limit_resources():
    # Limit memory to 500MB
    memory_limit = 500 * 1024 * 1024  # 500MB in bytes
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    # Limit CPU time to 5 seconds
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))


@app.post("/calculate")
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def calculate(request: Request, calculation_request: CalculationRequest):
    """
    Perform a numerical calculation based on the provided request.
    """
    try:
        logger.info(
            "calculation_started",
            service=calculation_request.service,
            calculation=calculation_request.calculation,
        )

        service = {
            "calculator": CalculatorService,
            "statistics": StatisticsService,
        }.get(calculation_request.service)

        if not service:
            raise ValueError(
                f"Service '{calculation_request.service}' is not supported"
            )

        # Run calculation with timeout
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                partial(
                    service.perform_calculation,
                    calculation_request.calculation,
                    calculation_request.data,
                    **calculation_request.params,
                ),
            ),
            timeout=5.0,
        )

        return {"result": result}

    except asyncio.TimeoutError:
        logger.error(
            "timeout_error",
            service=calculation_request.service,
            calculation=calculation_request.calculation,
        )
        raise HTTPException(status_code=408, detail="Calculation timed out")
    except Exception as e:
        logger.error("calculation_error", error=str(e), error_type=type(e).__name__)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    """
    Root endpoint of the API.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the FastAPI NumPy calculation server!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
