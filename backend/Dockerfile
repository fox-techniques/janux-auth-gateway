# Use an official Python runtime as a parent image
FROM python:3.10-slim

# It's a good practice to set a working directory for your application. This directory
# will be the base directory for all subsequent commands.
# Here, we ensure the working directory is explicitly set to where we intend to copy our application code.
WORKDIR /app

COPY ./backend/pyproject.toml ./backend/poetry.lock ./backend/README.md ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \  
    && poetry install --no-root

# Now copy the rest of your application code. This is done after the dependencies are installed
# to avoid invalidating Docker's cache every time any file changes, only the dependencies need reinstallation

COPY ./backend/app ./app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME FastAPI-Backend

# Run app.py when the container launches. Ensure the working directory is correctly set
# to where your application code resides, hence the WORKDIR command above is crucial.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
