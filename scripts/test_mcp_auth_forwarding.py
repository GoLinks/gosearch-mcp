import asyncio
import os

from fastmcp import Client


async def main() -> None:
    token = os.environ.get("TOKEN")
    if not token:
        raise SystemExit("Set TOKEN first: TOKEN='your-token' uv run python scripts/test_mcp_auth_forwarding.py")

    async with Client(
        "http://127.0.0.1:8000/mcp/",
        auth=token,
    ) as client:
        tools = await client.list_tools()
        print("tools:", [tool.name for tool in tools])

        result = await client.call_tool("search", {"query": "How do i reset my password?"})
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
