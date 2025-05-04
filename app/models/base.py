from datetime import datetime

from beanie import Document
from pydantic import Field


class BaseMongoDBModel(Document):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
