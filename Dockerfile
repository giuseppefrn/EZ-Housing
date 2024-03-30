# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Firefox and wget
RUN apt-get update \
    && apt-get install -y firefox-esr wget \
    && rm -rf /var/lib/apt/lists/*

# Download geckodriver and install it
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.30.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/

# Set the PATH environment variable to include the directory of geckodriver
ENV PATH="/usr/local/bin:${PATH}"

# Copy your project's 'pyproject.toml' and possibly 'poetry.lock' files
COPY pyproject.toml poetry.lock* ./

# Install Poetry
RUN pip install --no-cache-dir poetry

# Disable virtual env creation by Poetry, install dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the rest of your project's files into the container
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run your_script.py when the container launches
CMD ["python", "./src/extract.py", "--link", "https://www.pararius.com/apartments/leiden/700-1500/since-3"]
