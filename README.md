# GoSearch MCP Server

An MCP server that exposes [GoSearch](https://www.gosearch.ai) enterprise search as a tool for AI assistants. Built with [FastMCP](https://gofastmcp.com).

## Setup

Add this to your MCP client config (e.g., `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "gosearch": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GOSEARCH_API_TOKEN", "ghcr.io/golinks/gosearch-mcp"],
      "env": {
        "GOSEARCH_API_TOKEN": "YOUR_API_TOKEN"
      }
    }
  }
}
```

## Authentication

Generate a GoSearch API token from your workspace settings and set it as `GOSEARCH_API_TOKEN`.

## Tools

| Tool | Description |
|------|-------------|
| `search` | Search GoSearch for relevant results |