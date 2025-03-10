from abc import ABC, abstractmethod
from typing import List, Any, Union, Dict
import numpy as np


class BaseService(ABC):
    @staticmethod
    def _round_float(value: Any, decimals: int = 2) -> Any:
        """Round float values to specified decimal places."""
        if isinstance(value, float):
            return round(value, decimals)
        return value

    @classmethod
    def _convert_result(cls, result: Any) -> Any:
        """Convert result to JSON serializable format with rounded floats."""
        if isinstance(result, dict):
            return {k: cls._convert_result(v) for k, v in result.items()}
        elif isinstance(result, (list, tuple)):
            return [cls._convert_result(x) for x in list(result)]
        elif isinstance(result, np.generic):
            value = result.item()
            return cls._round_float(value)
        elif isinstance(result, np.ndarray):
            return [cls._round_float(x) for x in result.tolist()]
        return cls._round_float(result)

    @classmethod
    @abstractmethod
    def perform_calculation(
        cls, calculation: str, data: List[Any], **params: Dict[str, Any]
    ) -> Union[float, List[float]]:
        """
        Abstract method to perform calculations in derived services.

        Args:
            calculation: Name of the calculation to perform
            data: Input data for the calculation
            params: Additional parameters for the calculation

        Returns:
            Result as float or list of floats
        """
        pass
