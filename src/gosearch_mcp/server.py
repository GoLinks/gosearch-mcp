import fastmcp
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from gosearch_mcp.tools.goai import goai_response
from gosearch_mcp.tools.search import search

mcp = fastmcp.FastMCP("GoSearch")

mcp.add_tool(search)
mcp.add_tool(goai_response)


class RequireBearerOnMCP(BaseHTTPMiddleware):
    """Return 401 + WWW-Authenticate on /mcp when no Bearer token is present.

    Without this, MCP clients (e.g. Claude) skip OAuth discovery and treat the
    connector as unauthenticated.
    """

    def __init__(self, app: ASGIApp, resource_metadata_url: str) -> None:
        super().__init__(app)
        self._resource_metadata_url = resource_metadata_url

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path == "/mcp":
            auth = request.headers.get("authorization", "")
            if not auth.lower().startswith("bearer "):
                return JSONResponse(
                    {"error": "unauthorized"},
                    status_code=401,
                    headers={
                        "WWW-Authenticate": (
                            f'Bearer realm="GoSearch MCP", '
                            f'resource_metadata="{self._resource_metadata_url}"'
                        )
                    },
                )
        return await call_next(request)


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET"])
async def oauth_protected_resource_metadata(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "resource": "https://mcp.gosearch.ai",
            "authorization_servers": ["https://mcp.gosearch.ai"],
            "scopes_supported": ["search:read", "goai:read"],
            "bearer_methods_supported": ["header"],
        }
    )


@mcp.custom_route("/.well-known/oauth-protected-resource/mcp", methods=["GET"])
async def oauth_protected_resource_metadata_mcp(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "resource": "https://mcp.gosearch.ai/mcp",
            "authorization_servers": ["https://mcp.gosearch.ai"],
            "scopes_supported": ["search:read", "goai:read"],
            "bearer_methods_supported": ["header"],
        }
    )


@mcp.custom_route("/.well-known/oauth-authorization-server", methods=["GET"])
async def oauth_authorization_server_metadata(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "issuer": "https://www.gosearch.ai",
            "authorization_endpoint": "https://www.gosearch.ai/oauth/authorize",
            "token_endpoint": "https://www.gosearch.ai/d/api/oauth/token",
            "revocation_endpoint": "https://www.gosearch.ai/d/api/oauth/revoke",
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code", "refresh_token"],
            "code_challenge_methods_supported": ["S256"],
            "token_endpoint_auth_methods_supported": ["none"],
            "scopes_supported": [
                "search:read",
                "goai:read",
            ],
        }
    )
