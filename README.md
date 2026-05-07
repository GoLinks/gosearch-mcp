# GoSearch MCP Server

An MCP server that exposes [GoSearch](https://www.gosearch.ai) enterprise search and GoAI as tools for AI assistants. Built with [FastMCP](https://gofastmcp.com).

## Hosted HTTP Mode

This server is intended to run as a hosted remote MCP server over Streamable HTTP.

Public endpoint shape:

```text
https://mcp.gosearch.ai/mcp/
```

Local development endpoint shape:

```text
http://localhost:8000/mcp/
```

## Authentication

The hosted server does not use a shared `GOSEARCH_API_TOKEN`.

MCP clients should send a per-user GoSearch OAuth/API bearer token with each request:

```http
Authorization: Bearer YOUR_TOKEN
```

The MCP server forwards that header to `api.gosearch.ai`. GoSearch remains responsible for token validation, scope enforcement, refresh, storage, and revocation.

## Local Development

This project uses Python `3.12` and [`uv`](https://docs.astral.sh/uv/).

1. Install Python `3.12`.
2. Install `uv`.
3. Create the local environment and install dependencies:

```bash
uv sync
```

4. Run the MCP server locally:

```bash
uv run fastmcp run src/gosearch_mcp/server.py \
  --transport streamable-http \
  --host 0.0.0.0 \
  --port 8000 \
  --path /mcp/
```

5. Verify health and OAuth discovery:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/.well-known/oauth-authorization-server
```

## Docker

Build and run locally:

```bash
docker build -t gosearch-mcp .
docker run --rm -p 8000:8000 gosearch-mcp
```

## Tools

| Tool | Description |
|------|-------------|
| `search` | Search GoSearch for relevant results |
| `goai_response` | Get an AI-generated response from GoAI |
