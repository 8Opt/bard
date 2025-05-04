import time
import traceback
from typing import Optional

import httpx

from app.core.config import settings
from app.modules.tools.searchers.base_searcher import BaseSearcher
from app.models.tools import TDocuments

JINA_ENDPOINT = "https://r.jina.ai"

class JinaSearcher(BaseSearcher): 
    def __init__(self, api_key: Optional[str] = None): 
        super().__init__(name="JinaSearcher", api_key=api_key)

        self.api_key = api_key or settings.API_KEY_JINA

        if not self.api_key:
            raise ValueError(
                "Jina API key is required. Set it via environment variable or pass it explicitly."
            )

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def search(
        self,
        query: str,
        **kwargs
    ) -> TDocuments:


        url = JINA_ENDPOINT + f"/{query}"
        try:
            start_time = time.perf_counter()
            with httpx.Client(headers=self.headers) as client: 
                response = client.request(method="GET", url=url, headers=self.headers)
                response.raise_for_status()
            results = response.json().get('data', [])

            total_time = time.perf_counter() - start_time

            return TDocuments(
                query=query,
                topics=[results.get('title')],
                mode="",
                sources=[results.get('url')],
                total_time=int(total_time * 1000),
                metadata=results,
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
            mode="",
            sources=[],
            total_time=0,
            metadata={},
        )