FROM python:3.12.7-slim AS base

ENV TZ="Europe/Moscow"

RUN apt-get update && apt-get install -y --no-install-recommends curl wget

# Установка dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz \
    && rm dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml .

RUN poetry lock --no-cache && \
    poetry install --no-cache && \
    poetry cache clear pypi --all && \
    poetry cache clear virtualenvs --all && \
    pip cache purge && \
    find / -type f -name '*.py[cod]' -delete && \
    find / -type f -name '*.whl' -delete

COPY /src ./src

CMD ["dockerize", "-wait", "tcp://database:27017", "-timeout", "30s", "sh", "-c", "python -m uvicorn src.main:app --host $BACKEND_HOST --port $BACKEND_PORT"]