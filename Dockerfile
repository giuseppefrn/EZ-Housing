# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables to make Firefox run in headless mode
ENV MOZ_HEADLESS=1

# Update and install system packages
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Download and install geckodriver for ARM64
RUN wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux-aarch64.tar.gz \
    && tar -xvzf geckodriver.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/

# Copy the rest of the application into the container
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
