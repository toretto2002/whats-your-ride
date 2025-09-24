FROM python:3.12-slim-bookworm

# Install Poetry + debugpy
RUN pip install --no-cache-dir poetry debugpy

WORKDIR /app

COPY pyproject.toml poetry.lock* README.md /app/
COPY recommender_app /app/recommender_app

# Playwright deps (come in origine)
RUN apt-get update && \
    apt-get install -y wget gnupg ca-certificates && \
    apt-get install -y \
        libnspr4 \
        libnss3 \
        libdbus-1-3 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libxkbcommon0 \
        libatspi2.0-0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        libgbm1 \
        libasound2 \
    && rm -rf /var/lib/apt/lists/*

RUN poetry config virtualenvs.create false \
  && poetry lock \
  && poetry install --no-interaction --no-ansi

RUN playwright install --with-deps

COPY . /app
COPY docker/entrypoint.sh /app/docker/entrypoint.sh

RUN chmod +x /app/docker/entrypoint.sh

ENV FLASK_APP=run
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV DEBUG_PORT=5678

EXPOSE 5000 5678

ENTRYPOINT ["/app/docker/entrypoint.sh"]
