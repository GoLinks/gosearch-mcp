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

## Local Development

For local development, this project uses Python `3.12` and [`uv`](https://docs.astral.sh/uv/).

1. Install Python `3.12`.
2. Install `uv`.
3. Create the local environment and install dependencies:

```bash
uv sync
```

4. Export a GoSearch API token:

```bash
export GOSEARCH_API_TOKEN="YOUR_API_TOKEN"
```

5. Run the MCP server locally:

```bash
uv run fastmcp run src/gosearch_mcp/server.py
```

If you want to point Cursor at your local checkout while developing, use a config like this:

```json
{
  "mcpServers": {
    "gosearch": {
      "command": "uv",
      "args": [
        "run",
        "fastmcp",
        "run",
        "/absolute/path/to/gosearch-mcp/src/gosearch_mcp/server.py"
      ],
      "env": {
        "GOSEARCH_API_TOKEN": "YOUR_API_TOKEN"
      }
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `search` | Search GoSearch for relevant results |