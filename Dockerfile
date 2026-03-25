FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin appuser

COPY --chown=appuser:appuser pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY --chown=appuser:appuser src/ src/

USER appuser

CMD ["uv", "run", "fastmcp", "run", "src/gosearch_mcp/server.py"]