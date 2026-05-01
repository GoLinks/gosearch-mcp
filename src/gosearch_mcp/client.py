import httpx
from fastmcp import Context

GOSEARCH_API_URL = "https://api.gosearch.ai"

http_client = httpx.AsyncClient(
    base_url=GOSEARCH_API_URL,
    timeout=30,
)


def get_authorization_header(ctx: Context) -> str:
    """Return the incoming request Authorization header for forwarding to GoSearch APIs."""
    if ctx.request_context is None or ctx.request_context.request is None:
        raise PermissionError("Missing request context.")

    authorization = ctx.request_context.request.headers.get("authorization")
    if not authorization or not authorization.lower().startswith("bearer "):
        raise PermissionError("Missing bearer token.")

    return authorization
