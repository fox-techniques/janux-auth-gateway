# 📥 Installation

## 📦 pip 

**JANUX Authentication Gateway** is published as a python package and can be installed with
`pip`, ideally by using a [virtual environment]. Open up a terminal and install with:

=== "Latest"

    ``` sh
    pip install janux-auth-gateway
    ```

=== "1.x"

    ``` sh
    pip install janux-auth-gateway=="1.*" # (1)!
    ```

    1.  **JANUX** uses [semantic versioning].

        This will make sure that you don't accidentally [upgrade to the next
        major version], which may include breaking changes that silently corrupt
        your site. Additionally, you can use `pip freeze` to create a lockfile,
        so builds are reproducible at all times:

        ```
        pip freeze > requirements.txt
        ```

        Now, the lockfile can be used for installation:

        ```
        pip install -r requirements.txt
        ```

This will automatically install compatible versions of all dependencies:
[fastapi], [uvicorn], [pymongo], [motor] and [requests]. **JANUX** always strives to support the latest versions, so there's no need to
install those packages separately.

---

## 🎭 Poetry 

**JANUX** recommends using Poetry for its outstanding dependency management, use:

```bash
poetry add janux-auth-gateway

```

This command downloads and installs the package and its dependencies and adds the package as a dependency in your `pyproject.toml`.

After installation, you can start using the package in your project. If you need to enter the virtual environment managed by Poetry, run:

```bash
poetry shell

```

Verify the Installation:

```bash
poetry show janux-auth-gateway

```

Updating the Package:

```bash
poetry update janux-auth-gateway
```

---


## 🐙 GitHub

**JANUX** can be directly used from [GitHub] by cloning the
repository into a subfolder of your project root which might be useful if you
want to use the very latest version:

```bash
git clone https://github.com/fox-techniques/janux-auth-gateway.git
cd janux-auth-gateway
pip install -e .

```

---


## 🐳 Docker

**JANUX** can be run as a Standalone Docker Container with MongoDB & Redis.

➊ Check If **MongoDB & Redis** Are Already Running

Before running **JANUX**, ensure MongoDB and Redis are running.

```bash
docker ps
```

✅ Expected Output:

|CONTAINER ID  | IMAGE        | STATUS       | PORTS |
|---|---|---|---|
|abc123xyz     | mongo:latest | Up 10 minutes| 27017->27017/tcp|
|def456uvw     | redis:latest | Up 10 minutes| 6379->6379/tcp|

???+ failure "FAILED"

    🚨 If **MongoDB or Redis** is missing, start them manually:

    ```bash
    docker run -d --name mongodb -p 27017:27017 mongo:latest
    docker run -d --name redis -p 6379:6379 redis:latest
    ```

➋  Create a **Shared Docker Network**

Since MongoDB and Redis are in bridge mode, but JANUX needs to communicate with them, we must create a shared network.

```bash
docker network create janux-network
```

✅ Expected Output:

|NETWORK ID    | NAME           | DRIVER   | SCOPE|
|---|---|---|---|
|a1b2c3d4e5f6  | janux-network  | bridge   | local|

✅ Connect MongoDB & Redis to janux-network

```bash
docker network connect janux-network mongodb
docker network connect janux-network redis
```

✅ Now,** MongoDB and Redis** are reachable inside **janux-network.** To verify:

```bash
docker network inspect janux-network | grep '"Name":'
```

???+ failure "FAILED"

    🚨 If MongoDB is missing from the network, rerun:

    ```bash
    docker network connect janux-network mongodb
    ```

➍ Build **JANUX Authentication Gateway** Docker Image

Ensure the JANUX Docker image is up-to-date:
```bash
docker build -t janux-auth-gateway-standalone .
```

➎ Run **JANUX Standalone**

Now, start **JANUX** inside **janux-network** and mount secrets correctly. Run **JANUX with Correct Networking & Secrets**

```bash
docker run -p 8000:8000 \
  --network janux-network \
  -e MONGO_URI="mongodb://mongodb:27017/users_db" \
  -e REDIS_HOST="redis" \
  -e REDIS_PORT="6379" \
  -v $(pwd)/secrets:/run/secrets:ro \
  janux-auth-gateway
```



---

## 🚢 Docker Swarm (RECOMMENEDED)

Secrets ensure sensitive information (like private keys and database credentials) is securely stored. For multi-container setups including **MongoDB** and **Redis**: 

!!! danger "ATTENTION"

    Make sure you have **JANUX** configured with `.env`. If not, please go to the section [configuration](configuration.md).


➊ **Grant permissions**

First, first make sure permissions are set by running the following command in the terminal:

```bash
chmod +x ./setup_docker_secret.sh
```

➋ **Configure Docker Secrets**

Next, to create secrets, run the following command in the terminal:

```bash
./setup_docker_secret.sh
```

This script will:

- Check if Docker Swarm is initialized
- Create/update required secrets for authentication and database access

➌ **Verify Secrets**

```bash
docker secret ls
```

✅ *Expected Output:*


|ID|NAME|CREATED|UPDATED|
|---|---|---|---|
|xyz987xyz123|jwt_private_key|2 minutes ago|2 minutes ago|
|abc123abc456|jwt_public_key|2 minutes ago|2 minutes ago|

➍ **Deploy the Stack**

Run:

```bash
docker stack deploy -c docker-compose.yml janux-stack
```

This will:

- Deploy **JANUX Authentication Gateway**
- Deploy **MongoDB** and **Redis** as dependencies
- Ensure all services are properly networked

➎ **Check If Services Are Running**

Verify that all services are running with:

```bash
docker service ls
```

✅  *Expected Output:*

|ID|NAME|MODE|REPLICAS|IMAGE|PORTS|
|---|---|---|---|---|---|
|xyz987xyz|janux-stack_janux-auth-gateway|replicated|1/1|janux-auth-gateway:latest|*:8000->8000/tcp|
|uvw654uvw|janux-stack_mongodb|replicated|1/1|mongo:6.0||
|abc321abc|janux-stack_redis|replicated|1/1|redis:latest||                

???+ failure "FAILED"

    🚨 If the janux-auth-gateway service is 0/1, check logs:

    ```bash
    docker service logs -f janux-stack_janux-auth-gateway
    ```


➏ **Test the API**

Once all services are running, check the API health:

```bash
curl http://localhost:8000/health
```

✅ *Expected Output:*

```json
{"status": "healthy"}
```

➐ **Stop & Remove the Stack**

If you need to stop the application, run:

```bash
docker stack rm janux-stack

```

---

🤩 **CONGRAGULATIONS!** Continue to the **usage**. Let's keep going...🚀

  [JANUX-Auth-Gateway]: https://pypi.org/project/janux-auth-gateway/
  [GitHub]: https://github.com/fox-techniques/janux-auth-gateway
  [fastapi]: https://fastapi.tiangolo.com/
  [uvicorn]: https://www.uvicorn.org/
  [pymongo]: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/
  [motor]: https://motor.readthedocs.io/en/stable/
  [requests]: https://pypi.org/project/requests/
  [Poetry]: https://python-poetry.org/docs/#installation
  [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment
  [semantic versioning]: https://semver.org/
  [Using Python's pip to Manage Your Projects' Dependencies]: https://realpython.com/what-is-pip/