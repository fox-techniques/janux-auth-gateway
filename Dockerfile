# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && poetry install --no-root --no-dev

# Copy the application
COPY janux_auth_gateway /app/janux_auth_gateway

# Set environment variables to production
ENV ENVIRONMENT=production

# Expose the application port
EXPOSE 8000

# Use a start command that loads environment secrets
CMD ["poetry", "run", "uvicorn", "janux_auth_gateway.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
