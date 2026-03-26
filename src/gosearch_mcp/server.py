import fastmcp

from gosearch_mcp.tools.search import search

mcp = fastmcp.FastMCP("GoSearch")

mcp.add_tool(search)
