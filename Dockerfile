FROM python:3.13

# Install Poetry
RUN pip install poetry

# Set workdir
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* README.md /app/

# Copy package folder BEFORE poetry install (only what's needed)
COPY recommender_app /app/recommender_app

# Install deps and package
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the rest (e.g. tests, scripts)
COPY . /app

ENV FLASK_APP=run
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
