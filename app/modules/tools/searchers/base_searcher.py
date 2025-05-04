from abc import ABC, abstractmethod
from typing import Any, Optional

from app.core import setup_logger

class BaseSearcher(ABC):
    __slots__ = ['name', 'api_key']
    def __init__(self, api_key: Optional[str], name: str = "BaseSearcher"):
        self.logger = setup_logger(name=f"[{name}]")
        self.name = name 
        self.api_key = api_key

    @abstractmethod
    def search(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


    # TODO: add async search
    # TODO: stricly type-hint