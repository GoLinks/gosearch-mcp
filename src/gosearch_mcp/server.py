import fastmcp

from gosearch_mcp.tools.goai import goai_response
from gosearch_mcp.tools.search import search

mcp = fastmcp.FastMCP("GoSearch")

mcp.add_tool(search)
mcp.add_tool(goai_response)
