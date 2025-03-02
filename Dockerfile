FROM mcr.microsoft.com/playwright:v1.50.1-noble

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src

CMD ["uv", "run", "-m", "src.main"]
