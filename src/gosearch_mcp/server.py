import fastmcp
from starlette.requests import Request
from starlette.responses import JSONResponse

from gosearch_mcp.tools.goai import goai_response
from gosearch_mcp.tools.search import search

mcp = fastmcp.FastMCP("GoSearch")

mcp.add_tool(search)
mcp.add_tool(goai_response)


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


@mcp.custom_route("/.well-known/oauth-authorization-server", methods=["GET"])
async def oauth_authorization_server_metadata(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "issuer": "https://www.gosearch.ai",
            "authorization_endpoint": "https://www.gosearch.ai/d/api/oauth/authorize",
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
