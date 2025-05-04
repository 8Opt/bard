import time
import traceback
from typing import Literal, Optional
import httpx

from app.core.config import settings    
from app.models.tools import TDocuments
from app.modules.tools.searchers.base_searcher import BaseSearcher

LINKUP_ENDPOINT = "https://api.linkup.so/v1"


class LinkupSearcher(BaseSearcher):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(name="LinkupSearcher")

        self.api_key = api_key or settings.API_KEY_LINKUP

        if not self.api_key:
            raise ValueError(
                "LinkUp API key is required. Set it via environment variable or pass it explicitly. Visit https://app.linkup.so/api-keys to get one!"
            )

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def search(
        self,
        query: str,
        depth: Literal["standard", "deep"] = "standard",
        output_type: Literal[
            "sourcedAnswer", "searchResults", "structured"
        ] = "sourcedAnswer",
        structured_output_schema: str = "",
        includeImages: bool = False,
    ) -> TDocuments:
        payload = {
            "q": query,
            "depth": depth,
            "outputType": output_type,
            "structuredOutputSchema": structured_output_schema,
            "includeImages": includeImages,
        }

        url = LINKUP_ENDPOINT + "/search"
        try:
            start_time = time.perf_counter()
            with httpx.Client(headers=self.headers) as client: 
                response = client.request(method="POST", url=url, headers=self.headers, json=payload)
                response.raise_for_status()
            data = response.json()

            total_time = time.perf_counter() - start_time

            urls = [item["url"] for item in data.get("results", [])]

            return TDocuments(
                query=query,
                topics=[],
                mode=depth,
                sources=urls,
                total_time=int(total_time * 1000),
                metadata=data,
            )

        except httpx.HTTPStatusError as http_err:
            self.logger.warning(
                f"HTTP error {response.status_code} in {self.name}: {http_err.response.text}"
            )
        except httpx.RequestError as req_err:
            self.logger.warning(f"Request error in {self.name}: {req_err}")
        except Exception as e:
            self.logger.warning(
                f"Unexpected error in {self.name}: {e} || Traceback: {traceback.format_exc()}"
            )

        return TDocuments(
            query=query,
            topics=[],
            mode=depth,
            sources=[],
            total_time=0,
            metadata={},
        )
