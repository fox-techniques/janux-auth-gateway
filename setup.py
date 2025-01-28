from setuptools import setup, find_packages

# Load the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="janux-auth-gateway",
    version="0.1.0",
    author="FOX Techniques",
    author_email="ali.nabbi@fox-techniques.com",
    description="A modular authentication gateway for FastAPI microservices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fox-techniques/janux-auth-gateway",
    packages=find_packages(include=["janux_auth_gateway", "janux_auth_gateway.*"]),
    install_requires=[
        "fastapi>=0.92.0",
        "uvicorn>=0.18.3",
        "jose>=3.3.0",
        "passlib>=1.7.4",
        "motor>=3.1.0",
        "pydantic>=1.10.2",
        "python-dotenv>=0.21.0",
    ],
    extras_require={
        "dev": ["pytest>=8.3.3", "black>=23.1.0", "isort>=5.12.0"],
        "docs": ["mkdocs>=1.4.0", "mkdocs-material>=9.0.0"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.10",
    include_package_data=True,  # Ensures non-code files in MANIFEST.in are included
)
