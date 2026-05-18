import asyncio
import os

from starlette.middleware import Middleware

from gosearch_mcp.server import RequireBearerOnMCP, mcp


def main() -> None:
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8000"))
    resource_metadata_url = os.environ.get(
        "MCP_RESOURCE_METADATA_URL",
        "https://mcp.gosearch.ai/.well-known/oauth-protected-resource/mcp",
    )

    asyncio.run(
        mcp.run_http_async(
            transport="streamable-http",
            host=host,
            port=port,
            path="/mcp",
            middleware=[
                Middleware(
                    RequireBearerOnMCP,
                    resource_metadata_url=resource_metadata_url,
                )
            ],
            show_banner=False,
        )
    )


if __name__ == "__main__":
    main()
