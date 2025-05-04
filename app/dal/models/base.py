from datetime import datetime

from beanie import Document
from pydantic import Field


class BaseBeanieDBModel(Document):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
