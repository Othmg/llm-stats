from .base_service import BaseService
import numpy as np
from typing import Any, Union, List


class CalculatorService(BaseService):
    # Define the allowed numpy functions as a class attribute
    ALLOWED_FUNCTIONS = {
        "sum": np.sum,
        "mean": np.mean,
        "std": np.std,
        "min": np.min,
        "max": np.max,
        "median": np.median,
        "prod": np.prod,
        "var": np.var,
        "cumsum": np.cumsum,
        "cumprod": np.cumprod,
        "diff": np.diff,
        "abs": np.abs,
        "sqrt": np.sqrt,
        "log": np.log,
        "log10": np.log10,
        "exp": np.exp,
        "floor": np.floor,
        "ceil": np.ceil,
        "round": np.round,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "arcsin": np.arcsin,
        "arccos": np.arccos,
        "arctan": np.arctan,
        "square": np.square,
    }

    @classmethod
    def perform_calculation(
        cls, calculation: str, data: List[Any]
    ) -> Union[float, List[float]]:
        """
        Perform the specified calculation on the input data.

        Args:
            calculation: Name of the calculation to perform
            data: Input data for the calculation

        Returns:
            The calculation result as a number or list

        Raises:
            ValueError: If calculation is not supported or data format is invalid
        """
        if calculation not in cls.ALLOWED_FUNCTIONS:
            raise ValueError(f"Calculation '{calculation}' is not supported.")

        array = np.array(data)
        result = cls.ALLOWED_FUNCTIONS[calculation](array)

        # Convert numpy types to Python native types
        if isinstance(result, np.generic):
            return result.item()
        elif isinstance(result, np.ndarray):
            return result.tolist()
        return result
