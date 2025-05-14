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

## 🚢 Docker Swarm (RECOMMENEDED) 

### 🐘 PostgreSQL

Secrets ensure sensitive information (like private keys and database credentials) is securely stored. For multi-container setups including **PostgreSQL** and **Redis**: 

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
./setup_docker_secret.sh postgres
```


➌ **Deploy the Stack**

Run:

```bash
./deploy_janux_stack.sh docker-compose.postgres.yml

```

This will:

- Deploy **JANUX Authentication Gateway**
- Deploy **PostgreSQL** and **Redis** as dependencies
- Ensure all services are properly networked

➎ **Check If Services Are Running**

Verify that all services are running with:

```bash
docker service ls
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

### 🌱 MongoDB

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
./setup_docker_secret.sh mongo
```


➌ **Deploy the Stack**

Run:

```bash
./deploy_janux_stack.sh docker-compose.mongo.yml

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