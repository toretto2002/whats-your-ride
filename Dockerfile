FROM python:3.13

# Install Poetry
RUN pip install poetry

# Set workdir
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* README.md /app/

# Copy package folder BEFORE poetry install (only what's needed)
COPY recommender_app /app/recommender_app

# Installa dipendenze per Playwright headless browsers
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


# Install deps and package
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Install Playwright and its dependencies
RUN playwright install --with-deps


# Copy the rest (e.g. tests, scripts)
COPY . /app

ENV FLASK_APP=run
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
