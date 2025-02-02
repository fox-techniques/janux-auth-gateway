# Configuration 

## with pip <small>recommended</small> { #with-pip data-toc-label="with pip" }

JANUX-Auth-Gateway is published as a python package and can be installed with
`pip`, ideally by using a [virtual environment]. Open up a terminal and install
JANUX-Auth-Gateway with:

=== "Latest"

    ``` sh
    pip install janux-auth-gateway
    ```

=== "1.x"

    ``` sh
    pip install janux-auth-gateway=="1.*" # (1)!
    ```

    1.  JANUX uses [semantic versioning].

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
[fastapi], [uvicorn], [pymongo], [motor] and [requests]. JANUX Authentication Gateway always strives to support the latest versions, so there's no need to
install those packages separately.

---

!!! tip

    If you don't have prior experience with Python, we recommend reading
    [Using Python's pip to Manage Your Projects' Dependencies], which is a
    really good introduction on the mechanics of Python package management and
    helps you troubleshoot if you run into errors.

  [Python package]: https://pypi.org/project/janux-auth-gateway/
  [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment
  [semantic versioning]: https://semver.org/
  [Using Python's pip to Manage Your Projects' Dependencies]: https://realpython.com/what-is-pip/


## with git

JANUX authentication gateway can be directly used from [GitHub] by cloning the
repository into a subfolder of your project root which might be useful if you
want to use the very latest version:

```
git clone https://github.com/fox-techniques/janux-auth-gateway.git
```

Next, install the theme and its dependencies with:

```
pip install -e janux-auth-gateway
```

## with poetry

Prerequisites:

- Python 3.10 or higher
- [Poetry]

Installing JANUX Authentication Gateway:

```bash
poetry add janux-auth-gateway
```

This command downloads and installs the package and its dependencies and adds the package as a dependency in your `pyproject.toml`.

Using the Package:

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

  [JANUX-Auth-Gateway]: https://pypi.org/project/janux-auth-gateway/
  [GitHub]: https://github.com/fox-techniques/janux-auth-gateway

  [requests]: https://pypi.org/project/requests/
  [Poetry]: https://python-poetry.org/docs/#installation