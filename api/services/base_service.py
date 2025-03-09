from abc import ABC, abstractmethod
from typing import List, Any, Union


class BaseService(ABC):
    @classmethod
    @abstractmethod
    def perform_calculation(
        cls, calculation: str, data: List[Any]
    ) -> Union[float, List[float]]:
        pass
