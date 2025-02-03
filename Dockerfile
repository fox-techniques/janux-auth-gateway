# 🐍 Use an official lightweight Python image
FROM python:3.11-alpine AS runtime

# Set working directory inside the container
WORKDIR /app

# Install only essential runtime dependencies
RUN apk add --no-cache libffi openssl curl

# Install a minimal version of Poetry (binary only) & ensure it's in PATH
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy only necessary files for dependency resolution
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry (EXCLUDING dev, test, and docs)
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --without dev,docs

# Copy the actual application source code
COPY janux_auth_gateway/ /app/janux_auth_gateway/

# Ensure logs are stored in the correct location
RUN mkdir -p /var/log/janux && chmod -R 777 /var/log/janux

# Expose FastAPI port
EXPOSE 8000

# Set environment to container mode
ENV ENVIRONMENT=test

# 🏁 Start the FastAPI application (Correct Path)
CMD ["python", "-m", "janux_auth_gateway.main"]