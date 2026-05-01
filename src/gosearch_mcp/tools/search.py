from typing import Annotated

import httpx
from fastmcp import Context
from pydantic import BaseModel, Field

from gosearch_mcp.client import get_authorization_header, http_client


class GoLink(BaseModel):
    title: str = ""


class OwnerDetails(BaseModel):
    name: str = "Unknown"


class SearchResultMetadata(BaseModel):
    total_results: int = 0


class SearchResult(BaseModel):
    title: str = "No title"
    body: str = "No description available"
    url: str = ""
    service: str = "Unknown"
    owner_details: OwnerDetails = OwnerDetails()
    related_golinks: list[GoLink] = []


class SearchResponse(BaseModel):
    user_query: str = ""
    metadata: SearchResultMetadata = SearchResultMetadata()
    results: list[SearchResult] = []


async def search(
    query: Annotated[str, Field(description="The search query.", min_length=1)],
    service: Annotated[str | None, Field(description="Filter by service name (e.g. google-drive, slack, jira).")] = None,
    ctx: Context | None = None,
) -> str:
    """Search GoSearch for relevant results."""
    if ctx is None:
        raise PermissionError("Missing request context.")
    authorization = get_authorization_header(ctx)

    params = {
        k: v
        for k, v in {"q": query, "service": service, "limit": 10}.items()
        if v is not None
    }

    try:
        response = await http_client.get(
            "/search",
            params=params,
            headers={"Authorization": authorization},
        )
    except httpx.TimeoutException:
        raise TimeoutError("Request to GoSearch API timed out.")
    except httpx.ConnectError:
        raise ConnectionError("Failed to connect to GoSearch API.")

    if response.status_code == 401:
        raise PermissionError("Invalid or expired API token.")
    if response.status_code == 429:
        raise RuntimeError("Rate limit exceeded. Please try again later.")
    if response.status_code != 200:
        raise RuntimeError(f"GoSearch API returned status {response.status_code}.")

    return format_response(SearchResponse.model_validate(response.json()))


def format_response(data: SearchResponse) -> str:
    if not data.results:
        return "No results found."

    lines = [f'Search results for "{data.user_query}" ({data.metadata.total_results} results):\n']

    for i, result in enumerate(data.results, 1):
        entry = f"[{i}] {result.title}\n{result.body}\nSource: {result.service}\nOwner: {result.owner_details.name}\nURL: {result.url}"

        if result.related_golinks:
            links = ", ".join(gl.title for gl in result.related_golinks)
            entry += f"\nGoLinks: {links}"

        lines.append(entry)

    return "\n\n".join(lines)
