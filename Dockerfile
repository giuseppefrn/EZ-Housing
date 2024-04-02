# Start with the official Airflow image
FROM apache/airflow:2.9.0b2-python3.12

# Set environment variables (if needed, some might be better set in docker-compose.yml)
ENV MOZ_HEADLESS=1

USER root

# Update and install system packages
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install geckodriver for ARM64
RUN wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux-aarch64.tar.gz \
    && tar -xvzf geckodriver.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/

USER airflow

# Assuming you have a pyproject.toml and poetry.lock file in your project root.
COPY pyproject.toml poetry.lock /opt/airflow/

WORKDIR /opt/airflow

# Install Poetry and Python dependencies
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY dags /original/dags
COPY plugins /original/plugins
COPY src /original/src
