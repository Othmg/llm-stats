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

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, validator
from typing import List, Any, Literal
from services.numpy_llm import CalculatorService
from services.scipy_llm import StatisticsService
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog
from datetime import datetime
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import asyncio
from functools import partial
import resource

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

logger = structlog.get_logger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "www.statsforllm.com",  # Your production domain
        "*.vercel.app",  # Vercel preview deployments
        "localhost",  # Local development
        "127.0.0.1",  # Local development
    ],
)


class CalculationRequest(BaseModel):
    service: Literal["calculator", "statistics"]
    calculation: str
    data: List[Any]

    @validator("data")
    def validate_data(cls, v):
        if len(v) > 10000:  # Set reasonable limits
            raise ValueError("Data array too large")
        # Add size validation for individual numbers
        if any(abs(float(x)) > 1e308 for x in v if isinstance(x, (int, float))):
            raise ValueError("Numbers too large - must be within float64 range")
        # Add type validation
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError("All values must be numbers")
        return v


def limit_resources():
    # Limit memory to 500MB
    memory_limit = 500 * 1024 * 1024  # 500MB in bytes
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    # Limit CPU time to 5 seconds
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))


@app.post("/calculate")
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def calculate(request: CalculationRequest):
    """
    Perform a numerical calculation based on the provided request.
    """
    try:
        # Set resource limits before calculation
        limit_resources()

        service = {
            "calculator": CalculatorService,
            "statistics": StatisticsService,
        }.get(request.service)

        if not service:
            raise ValueError(f"Service '{request.service}' is not supported")

        # Run calculation with timeout
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                partial(service.perform_calculation, request.calculation, request.data),
            ),
            timeout=5.0,  # 5 second timeout
        )
        return {"result": result}
    except resource.error as e:
        raise HTTPException(
            status_code=429,
            detail={"error": "Resource limit exceeded", "message": str(e)},
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail={
                "error": "Calculation timeout",
                "message": "Calculation took too long",
            },
        )
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(
            status_code=400, detail={"error": "Invalid input", "message": str(e)}
        )
    except (TypeError, RuntimeError) as e:
        # Handle numpy/scipy specific errors
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Calculation error",
                "message": str(e),
                "calculation": request.calculation,
            },
        )
    except Exception as e:
        # Log unexpected errors
        logger.error(
            "calculation_error",
            service=request.service,
            calculation=request.calculation,
            error=str(e),
        )
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error", "message": str(e)},
        )


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
