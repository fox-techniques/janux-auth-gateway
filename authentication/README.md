# Getting Started with FastAPI

## Available Scripts

In the project directory, you can run:

### `uvicorn app.main:app --port 5000 --reload`

Runs the app in the development mode locally. Execute this command on the root folder of `app`.
Open [http://127.0.0.1:5000](http://127.0.0.1:5000/) to view it in your browser.

### `docker build -t backend-fastapi .`

Builds the docker image

### `docker run -d --name backend-fastapi-container -p 5000:5000 backend-fastapi`

Runs the application in docker container
