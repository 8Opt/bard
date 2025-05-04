from typing import Dict, List, Optional

from pydantic import Field

from app.dal.models.base import BaseMongoDBModel
from app.common.helpers import get_time_now

class TDocuments(BaseMongoDBModel):
    query: str
    topics: Optional[List[str]] = []
    mode: str
    sources: List[str] = []
    timestamp: int = Field(default_factory=get_time_now)
    metadata: Optional[Dict] = {}
