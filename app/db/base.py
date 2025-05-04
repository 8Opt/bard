from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar


ModelType = TypeVar("ModelType")


class BaseRepository(ABC, Generic[ModelType]):
    @abstractmethod
    async def create(self, data: dict) -> ModelType:
        pass

    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def get_multi(
        self,
        page: int = 1,
        page_size: int = 10,
        search: str = None,
        sort: dict = None,
        filters: dict = None,
    ) -> List[ModelType]:
        pass

    @abstractmethod
    async def update(self, obj: ModelType, data: dict) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def delete(self, obj: ModelType) -> bool:
        pass

