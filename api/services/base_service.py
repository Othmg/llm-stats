from abc import ABC, abstractmethod
from typing import List, Any, Union, Dict


class BaseService(ABC):
    @classmethod
    @abstractmethod
    def perform_calculation(
        cls, calculation: str, data: List[Any], **params: Dict[str, Any]
    ) -> Union[float, List[float]]:
        pass
