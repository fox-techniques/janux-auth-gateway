# 🐍 Use an official lightweight Python image
FROM python:3.11-slim AS base

# Set working directory inside the container
WORKDIR /app

# Install required dependencies
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Copy only necessary files for dependency resolution
# Prevents errors if poetry.lock is missing
COPY pyproject.toml poetry.lock* ./

# Install dependencies using Poetry
RUN $HOME/.local/bin/poetry config virtualenvs.create false && \
    $HOME/.local/bin/poetry install --no-interaction --no-root --without dev

# Copy the application source code
COPY . .

# Ensure logs are stored in the correct location
RUN mkdir -p /var/log/janux && chmod -R 777 /var/log/janux

# Expose the FastAPI port
EXPOSE 8000

# Set environment to container mode
ENV ENVIRONMENT=test

# 🏁 Start the FastAPI application
CMD ["python", "-m", "janux_auth_gateway.app.main"]
