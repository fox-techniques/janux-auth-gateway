# ⚡️ Prerequisites

Before installing **JANUX**, ensure you have the following dependencies installed:

- Python 3.10+
- pip or Poetry 
- Git
- Docker
- MongoDB
- Redis

---

## 🐍 Python 3.10+

Ensure you have **Python 3.10+** installed. If not, download and install it from the [official Python website](https://www.python.org/downloads/). Check your version:

```bash
python --version
```
For installation guides and troubleshooting, refer to the [RealPython](https://realpython.com/installing-python/) documentation.

## 📦 Package managers

=== "pip"


    !!! info "Knowledge"

        If you don't have prior experience with Python, we recommend reading
        [Using Python's pip to Manage Your Projects' Dependencies], which is a
        really good introduction on the mechanics of Python package management and
        helps you troubleshoot if you run into errors.

    [Python package]: https://pypi.org/project/janux-auth-gateway/
    [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment
    [semantic versioning]: https://semver.org/
    [Using Python's pip to Manage Your Projects' Dependencies]: https://realpython.com/what-is-pip/

    Upgrade pip to the latest version: 

    ``` sh
    python -m pip install --upgrade pip
    ```

=== "Poetry"

    Install Poetry as package manager and dependencies management:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    

## 🌱 Git

Ensure you have **Git** installed. If not, download and install it from the [official Git website](https://git-scm.com/downloads). Check your version:

```bash
git --version
```

## 🐳 Docker & Docker Compose

To run **JANUX** Authentication Gateway using Docker, ensure you have Docker and Docker Compose installed. Download and install Docker from the official website:

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Docker Desktop](https://docs.docker.com/desktop/)

Verify installation with: 

```bash
docker version
```

```bash
docker compose version
```


## 🍃 MongoDB

**MongoDB** is required for storing user and admin credentials. We highly recommend to run a **MongoDB** instance in Docker. 

➊ Pull MongoDB docker image 

```bash
docker pull mongo
```
➋ Run MongoDB in a container

=== "MongoDB on Docker"

    To run a MongoDB instance in a container:

    ```bash
    docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=rootPassw0rd123! mongo
    ```

=== "Persistent MongoDB on Docker"

    **RECOMMENDED!** To persist data beyond container restarts, mount a local volume:

    ```bash
    docker run -d --name mongodb -p 27017:27017 -v mongodb_data:/data/db -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=rootPassw0rd123! mongo
    ```

➌ Connect to MongoDB instance 

```bash
mongosh --host localhost --port 27017 -u admin -p secret
```

Optionally, you can install [MongoDB Compass](https://www.mongodb.com/products/tools/compass) GUI for MongoDB.

➍ Stop and remove MongoDB

```bash
docker stop mongodb
docker rm mongodb
```

For a standalone installation please follow the [MongoDB Installation Guide](https://www.mongodb.com/docs/manual/installation/).

## 🔥 Redis

**Redis** is required for storing user and admin credentials. We highly recommend to run a **Redis** instance in Docker. 

➊ Pull Redis docker image 

```bash
docker pull redis
```
➋ Run Redis in a container

=== "Redis on Docker"

    To run a Redis instance in a container:

    ```bash
    docker run -d --name redis -p 6379:6379 redis
    ```

=== "Persistent Redis on Docker"

    **RECOMMENDED!** To persist data beyond container restarts, mount a local volume:

    ```bash
    docker run -d --name redis -p 6379:6379 -v redis_data:/data redis --save 60 1 --loglevel warning
    ```

=== "Redis with Authentication"

    **RECOMMENDED!** By default, Redis runs without a password. To add one:

    ```bash
    docker run -d --name redis -p 6379:6379 redis --requirepass "redisPassw0rd123!"
    ```

➌ Connect to Redis instance 

```bash
docker exec -it redis redis-cli
```

➍ Stop and remove Redis

```bash
docker stop redis
docker rm redis
```

For a standalone installation please follow the [Redis Installation Guide](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).

Now that prerequisites are set, continue with **configuration**. 🎯

  [JANUX-Auth-Gateway]: https://pypi.org/project/janux-auth-gateway/
  [GitHub]: https://github.com/fox-techniques/janux-auth-gateway
  [fastapi]: https://fastapi.tiangolo.com/
  [uvicorn]: https://www.uvicorn.org/
  [pymongo]: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/
  [motor]: https://motor.readthedocs.io/en/stable/
  [requests]: https://pypi.org/project/requests/
  [Poetry]: https://python-poetry.org/docs/#installation