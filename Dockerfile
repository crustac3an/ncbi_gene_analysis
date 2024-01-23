# Use a minimal Python image
FROM python:3.11.7-slim-bookworm

# Set working directory in the container
WORKDIR /app

# Install poetry
RUN pip install poetry

# Disable virtualenv creation by poetry
RUN poetry config virtualenvs.create false

# Copy only the pyproject.toml file
COPY pyproject.toml /app/

# Install dependencies using Poetry
# This will create a new poetry.lock file
RUN poetry install --no-interaction --no-ansi

# Copy the rest of your application
COPY . /app

# Start Jupyter Lab
CMD ["poetry", "run", "jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
