import re
from datetime import datetime
from typing import Generic, Optional, Type, TypeVar

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.core.config import settings
from app.models.base import BaseBeanieDBModel
from app.utils import setup_logger

logger = setup_logger(__name__)

ModelType = TypeVar("ModelType", bound=BaseBeanieDBModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseMongoDBRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model: Type[ModelType] = model
        self.unique_fields: list[str] = []
        self.searchable_fields: list[str] = []

    async def create(self, data: CreateSchemaType) -> ModelType:
        obj = self.model(**data.model_dump())
        return await obj.insert()

    async def get_by_id(self, id: PydanticObjectId) -> Optional[ModelType]:
        obj = await self.model.get(id)
        if obj:
            await obj.migrate_if_needed()
        return obj

    async def get_multi(
        self,
        page: int = 1,
        page_size: int = settings.PAGE_SIZE,
        search: str = None,
        sort: dict = None,
        filters: dict = None,
    ) -> List[ModelType]:
        """
        Get multiple documents with pagination, searching, and sorting.

        Note: We use raw MongoDB aggregation pipeline instead of Beanie's methods because:
        1. We need natural sorting (numericOrdering) for string fields containing numbers
        2. Beanie doesn't directly support collation settings
        3. Using motor_collection gives us more control over the query execution

        Args:
            page: Current page number (starts from 1)
            page_size: Number of items per page
            search: Search text to query across searchable fields
            sort: Dict containing field and direction for sorting (e.g. {"name": 1})
            filters: Dict containing filters to apply to the query

        Returns:
            PaginationResponse containing items and pagination info
        """
        page = max(page, 1)
        page_size = min(max(1, page_size), settings.MAX_PAGE_SIZE)
        skip = (page - 1) * page_size
        query_filters = filters or {}

        if search and self.searchable_fields:
            escaped_search = re.escape(search)
            search_conditions = []
            for field in self.searchable_fields:
                search_conditions.append(
                    {field: {"$regex": f".*{escaped_search}.*", "$options": "i"}}
                )
            if search_conditions:
                if len(search_conditions) > 1:
                    query_filters["$or"] = search_conditions
                else:
                    query_filters.update(search_conditions[0])

                logger.debug(f"Search text: {search}")
                logger.debug(f"Escaped search: {escaped_search}")
                logger.debug(f"Query filters: {query_filters}")

        # Build aggregation pipeline for more control over query execution
        # This allows us to use collation for natural sorting of strings containing numbers
        pipeline = [
            {"$match": query_filters},
        ]

        # Add sorting with natural collation
        # Example: "user10" will come after "user2" instead of before
        if sort:
            field = list(sort.keys())[0]
            order = list(sort.values())[0]
            if field and order is not None:
                pipeline.append({"$sort": {field: order}})

        pipeline.extend(
            [
                {"$skip": skip},
                {"$limit": page_size},
            ]
        )

        # Execute aggregation with collation for proper string sorting
        # locale: "en" - Use English locale rules
        # numericOrdering: True - Enable natural sorting for strings containing numbers
        collection = self.model.get_motor_collection()
        items = await collection.aggregate(
            pipeline, collation={"locale": "en", "numericOrdering": True}
        ).to_list(length=None)
        # Get total count for pagination
        total = await collection.count_documents(query_filters)

        # Calculate total pages
        total_pages = max(1, ((total - 1) // page_size) + 1)

        # Convert raw MongoDB documents back to Beanie models
        return items

    async def update(
        self, id: PydanticObjectId, data: UpdateSchemaType
    ) -> Optional[ModelType]:
        """
        Update a document by its ID with the provided data.
        """
        update_data = data.model_dump(exclude_unset=True)
        obj = await self.model.get(id)

        if not obj:
            logger.warning(f"Object with ID {id} not found.")
            return None

        if update_data:
            update_data["updated_at"] = datetime.now()

        await obj.set(update_data)
        return obj

    async def delete(self, id: PydanticObjectId) -> bool:
        """
        Delete a document by its ID.
        """
        obj = await self.model.get(id)

        if not obj:
            logger.warning(f"Object with ID {id} not found.")
            return False

        await obj.delete()
        return True
