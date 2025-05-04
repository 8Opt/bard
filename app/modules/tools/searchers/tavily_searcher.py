import time
import traceback
from typing import List, Literal, Optional

import httpx

from app.core.config import settings
from app.modules.tools.searchers.base_searcher import BaseSearcher
from app.models.tools import TDocuments
from app.common.helpers import get_time_now

TAVILY_ENDPOINT = "https://api.tavily.com"


class TavilySearcher(BaseSearcher):
    def __init__(self, api_key: str = None):
        """
        Initializes the TavilySearcher with an API key.

        Args:
            api_key (str): The Tavily API key. If not provided, it is retrieved from environment variables.
        """
        super().__init__(name="TavilySearcher")

        self.api_key = api_key or settings.API_KEY_TAVILY

        if not self.api_key:
            raise ValueError(
                "Tavily API key is required. Set it via environment variable or pass it explicitly. Visit https://app.tavily.com/home to get one!"
            )

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def search(
        self,
        query: str,
        topic: Literal["general", "news"] = "general",
        search_depth: Literal["basic", "advanced"] = "basic",
        max_results: int = 3,
        time_range: Optional[str] = None,
        days: int = 3,
        include_answer: bool = False,
        include_image_descriptions: bool = False,
        include_domains: List[str] = [],
        exclude_domains: List[str] = [],
    ) -> TDocuments:
        """
        Executes a search query using the Tavily API.

        Args:
            query (str): The search query.
            topic (Literal["general", "news"]): The topic of the search.
            search_depth (Literal["basic", "advanced"]): The depth of the search.
            max_results (int): The maximum number of results to return.
            time_range (Optional[str]): A time range filter (e.g., "past_week").
            days (int): Number of past days to consider.
            include_answer (bool): Whether to include AI-generated answers.
            include_image_descriptions (bool): Whether to include image descriptions.
            include_domains (Optional[List[str]]): Domains to prioritize.
            exclude_domains (Optional[List[str]]): Domains to exclude.

        Returns:
            Documents: A structured response containing search results.
        """
        payload = {
            "query": query,
            "topic": topic,
            "search_depth": search_depth,
            "max_results": max_results,
            "time_range": time_range,
            "days": days,
            "include_answer": include_answer,
            "include_image_descriptions": include_image_descriptions,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
        }
        url = TAVILY_ENDPOINT + "/search"

        try:

            with httpx.Client(headers=self.headers) as client: 
                response = client.request(method="POST", url=url, headers=self.headers, json=payload)
                response.raise_for_status()
            data = response.json()

            urls = [item["url"] for item in data.get("results", [])]

            return TDocuments(
                query=query,
                topics=[],
                mode=search_depth,
                sources=urls,
                timestamp=get_time_now(),
                total_time=data.get("response_time"),
                metadata=data,
            )

        except httpx.HTTPStatusError as http_err:
            self.logger.warning(
                f"HTTP error {response.status_code} in {self.name}: {http_err.response.text}"
            )
        except httpx.RequestError as req_err:
            self.logger.warning(f"Request error in  {self.name}: {req_err}")
        except Exception as e:
            self.logger.warning(
                f"Unexpected error in  {self.name}: {e} || Traceback: {traceback.format_exc()}"
            )

        return TDocuments(
            query=query,
            topics=[topic],
            mode=search_depth,
            sources=[],
            timestamp=get_time_now(),
            total_time=0,
            metadata={},
        )



    def extract(
        self,
        url: str,
        include_images: bool = False,
        extract_depth: Literal["basic", "advanced"] = "basic",
    ) -> TDocuments:
        """
        Extracts web page content from a specified URL using the Tavily Extract API.

        Args:
            url (str): The URL of the webpage to extract content from.
            include_images (bool): Whether to extract image descriptions.
            extract_depth (Literal["basic", "advanced"]): The extraction depth.

        Returns:
            TDocuments: A structured response containing extracted content.
        """
        payload = {
            "url": url,
            "include_images": include_images,
            "extract_depth": extract_depth,
        }
        endpoint = f"{TAVILY_ENDPOINT}/extract"

        try:
            start_time = time.perf_counter()
            response = httpx.post(url=endpoint, headers=self.headers, json=payload)
            total_time = time.perf_counter() - start_time

            response.raise_for_status()
            data = response.json().get("results", {})

            return TDocuments(
                query=url,
                topics=[],
                mode=extract_depth,
                sources=[url],
                timestamp=get_time_now(),
                total_time=int(total_time * 1000),  # Convert seconds to milliseconds
                metadata=data,
            )

        except httpx.HTTPStatusError as http_err:
            self.logger.warning(
                f"HTTP error {response.status_code} in  {self.name}: {http_err.response.text}"
            )
        except httpx.RequestError as req_err:
            self.logger.warning(f"Request error in  {self.name}: {req_err}")
        except Exception as e:
            self.logger.warning(
                f"Unexpected error in  {self.name}: {e} || Traceback: {traceback.format_exc()}"
            )

        return TDocuments(
            query=url,
            topics=[],
            mode=extract_depth,
            sources=[],
            timestamp=get_time_now(),
            total_time=0,
            metadata={},
        )
