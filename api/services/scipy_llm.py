from typing import List, Any, Union
import numpy as np
from scipy import stats
from api.services.base_service import BaseService


class StatisticsService(BaseService):
    ALLOWED_FUNCTIONS = {
        # Basic statistics
        "describe": stats.describe,
        # Correlation tests
        "pearsonr": lambda a, b: stats.pearsonr(a, b),
        # Regression
        "linregress": lambda x, y: stats.linregress(x, y)._asdict(),
    }

    # Special cases that require specific parameter handling
    SPECIAL_CASES = {
        "two_sample": [
            "pearsonr",
            "spearmanr",
        ],
        "regression": ["linregress"],
    }

    @classmethod
    def _handle_special_calculation(cls, calculation: str, data: dict):
        try:
            if calculation in cls.SPECIAL_CASES["regression"]:
                x = np.array(data.get("x"), dtype=float)
                y = np.array(data.get("y"), dtype=float)
                result = cls.ALLOWED_FUNCTIONS[calculation](x, y)
                return cls._convert_result(result)

            elif calculation in cls.SPECIAL_CASES["two_sample"]:
                a = np.array(data.get("a"), dtype=float)
                b = np.array(data.get("b"), dtype=float)
                result = cls.ALLOWED_FUNCTIONS[calculation](a, b)
                return cls._convert_result(result)

            raise ValueError(f"Unhandled special case for calculation: {calculation}")

        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Invalid data format: {str(e)}. All values must be numeric (integers or floats)."
            )

    @classmethod
    def perform_calculation(
        cls, calculation: str, data: Union[dict, List[Any]], **params
    ):
        try:
            # Handle special cases through _handle_special_calculation
            if any(calculation in cases for cases in cls.SPECIAL_CASES.values()):
                # No need for conversion, expect data in correct format
                return cls._handle_special_calculation(calculation, data)

            # For other calculations, convert data to float numpy array
            array = np.array(data, dtype=float)
            func = getattr(stats, calculation)
            result = func(array, **params)

            # Handle tuple returns
            if hasattr(result, "_fields"):  # Named tuple
                result = {field: getattr(result, field) for field in result._fields}
            elif isinstance(result, tuple):
                result = list(result)

            # Convert the result to ensure proper rounding
            return cls._convert_result(
                result
            )  # Add this line to ensure consistent rounding

        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Invalid data format: {str(e)}. All values must be numeric (integers or floats)."
            )
