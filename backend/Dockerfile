FROM python:3.12.7-slim AS base

ENV TZ="Europe/Moscow"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl

FROM base AS base_with_req

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml .

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH" && \
    poetry lock --no-cache && \
    poetry install --no-cache && \
    poetry cache clear pypi --all && \
    poetry cache clear virtualenvs --all && \
    pip cache purge && \
    find / -type f -name '*.py[cod]' -delete && \
    find / -type f -name '*.whl' -delete

FROM base_with_req

WORKDIR /app

COPY /src ./src

CMD ["sh", "-c", "python -m uvicorn src.main:app --host $APP_HOST --port $APP_PORT"]