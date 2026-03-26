import os
from typing import Annotated, Optional

import fastmcp
import httpx
from pydantic import Field
from pydantic import validate_call

mcp = fastmcp.FastMCP("GoSearch")

GOSEARCH_API_URL = "https://api.gosearch.ai"

http_client = httpx.AsyncClient(
    base_url=GOSEARCH_API_URL,
    timeout=30,
)

Category = Annotated[
    str,
    Field(
        pattern="^(files|tasks|people|golinks|answers|chats|images|events|all)$",
        description="Filter results by category.",
    ),
]

SortField = Annotated[
    str,
    Field(
        pattern="^(relevance|date_created|date_edited|weekly_hits)$",
        description="Sort results by field.",
    ),
]


@mcp.tool()
@validate_call
async def search(
    query: Annotated[str, Field(description="The search query.")],
    category: Optional[Category] = None,
    service: Annotated[
        Optional[str],
        Field(description="Filter by service name (e.g. google-drive, slack, jira)."),
    ] = None,
    sort: Optional[SortField] = None,
    limit: Annotated[
        int, Field(ge=1, le=100, description="Number of results to return.")
    ] = 10,
) -> dict:
    """Search GoSearch for relevant results."""
    token = os.environ.get("GOSEARCH_API_TOKEN")
    if not token:
        return {"error": "GOSEARCH_API_TOKEN environment variable is not set."}

    params = {"q": query, "limit": limit}
    if category:
        params["category"] = category
    if service:
        params["service"] = service
    if sort:
        params["sort"] = sort

    try:
        response = await http_client.get(
            "/search",
            params=params,
            headers={"Authorization": f"Bearer {token}"},
        )
    except httpx.TimeoutException:
        return {"error": "Request to GoSearch API timed out."}
    except httpx.ConnectError:
        return {"error": "Failed to connect to GoSearch API."}

    if response.status_code == 401:
        return {"error": "Invalid or expired API token."}
    if response.status_code == 429:
        return {"error": "Rate limit exceeded. Please try again later."}
    if response.status_code != 200:
        return {"error": f"GoSearch API returned status {response.status_code}."}

    return response.json()
