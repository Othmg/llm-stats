from .base_service import BaseService
import numpy as np
from typing import Any, Union, List, Dict, Callable


class CalculatorService(BaseService):
    # Define allowed functions with their descriptions
    ALLOWED_FUNCTIONS: Dict[str, Callable] = {
        # Basic Statistical
        "sum": np.sum,  # Sum of array elements
        "mean": np.mean,  # Arithmetic mean
        "std": np.std,  # Standard deviation
        "min": np.min,  # Minimum value
        "max": np.max,  # Maximum value
        "median": np.median,  # Median value
        "prod": np.prod,  # Product of array elements
        "percentile": np.percentile,  # Percentile
        "var": np.var,  # Variance
        # Array Operations
        "cumsum": np.cumsum,  # Cumulative sum
        "cumprod": np.cumprod,  # Cumulative product
        "diff": np.diff,  # Discrete difference
        # Mathematical Functions
        "abs": np.abs,  # Absolute value
        "sqrt": np.sqrt,  # Square root
        "log": np.log,  # Natural logarithm
        "log10": np.log10,  # Base-10 logarithm
        "exp": np.exp,  # Exponential
        # Rounding
        "floor": np.floor,  # Floor of each element
        "ceil": np.ceil,  # Ceiling of each element
        "round": np.round,  # Round to given decimals
        # Trigonometric
        "sin": np.sin,  # Sine
        "cos": np.cos,  # Cosine
        "tan": np.tan,  # Tangent
        "arcsin": np.arcsin,  # Inverse sine
        "arccos": np.arccos,  # Inverse cosine
        "arctan": np.arctan,  # Inverse tangent
        "square": np.square,  # Square each element
    }

    @classmethod
    def perform_calculation(
        cls, calculation: str, data: List[Any], **params: Dict[str, Any]
    ) -> Union[float, List[float]]:
        """
        Perform the specified calculation on the input data.

        Args:
            calculation: Name of the calculation to perform
            data: Input data for the calculation
            params: Additional parameters for the numpy function

        Returns:
            The calculation result as a number or list with floats rounded to 2 decimal places

        Raises:
            ValueError: If calculation is not supported or data format is invalid
        """
        if calculation not in cls.ALLOWED_FUNCTIONS:
            raise ValueError(
                f"Calculation '{calculation}' is not supported. "
                f"Allowed calculations: {', '.join(sorted(cls.ALLOWED_FUNCTIONS.keys()))}"
            )

        array = np.array(data)
        result = cls.ALLOWED_FUNCTIONS[calculation](array, **params)

        return cls._convert_result(result)
