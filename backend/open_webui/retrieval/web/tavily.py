import logging
<<<<<<< HEAD
from typing import Optional
=======
>>>>>>> dfef03c8e (同步远程)

import requests
from open_webui.retrieval.web.main import SearchResult
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


<<<<<<< HEAD
def search_tavily(
    api_key: str,
    query: str,
    count: int,
    filter_list: Optional[list[str]] = None,
    # **kwargs,
) -> list[SearchResult]:
=======
def search_tavily(api_key: str, query: str, count: int) -> list[SearchResult]:
>>>>>>> dfef03c8e (同步远程)
    """Search using Tavily's Search API and return the results as a list of SearchResult objects.

    Args:
        api_key (str): A Tavily Search API key
        query (str): The query to search for

    Returns:
        list[SearchResult]: A list of search results
    """
    url = "https://api.tavily.com/search"
    data = {"query": query, "api_key": api_key}
<<<<<<< HEAD
=======

>>>>>>> dfef03c8e (同步远程)
    response = requests.post(url, json=data)
    response.raise_for_status()

    json_response = response.json()

    raw_search_results = json_response.get("results", [])

    return [
        SearchResult(
            link=result["url"],
            title=result.get("title", ""),
            snippet=result.get("content"),
        )
        for result in raw_search_results[:count]
    ]
