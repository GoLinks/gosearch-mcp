import fastmcp

mcp = fastmcp.FastMCP("GoSearch")


@mcp.tool()
async def search(query: str) -> str:
    """Search GoSearch for relevant results."""
    return "Not implemented yet"
