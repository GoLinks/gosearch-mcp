import os

import httpx

GOSEARCH_API_URL = "https://api.gosearch.ai"

http_client = httpx.AsyncClient(
    base_url=GOSEARCH_API_URL,
    timeout=30,
)


def get_api_token() -> str:
    token = os.environ.get("GOSEARCH_API_TOKEN")
    if not token:
        raise ValueError("GOSEARCH_API_TOKEN environment variable is not set.")
    return token
