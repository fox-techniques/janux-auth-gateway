# 🔧 Configuration 

**JANUX Authentication Gateway** relies on environment variables and Docker secrets to securely store configuration values. Below is a guide on how to configure the service.


## 🌍 Environment Variables 

For non-sensitive settings, **JANUX** loads configuration from a `.env` file or system environment variables. The following default `.env.example` file is provided for local development. 

```bash title=".env"
# ========================
# 🌍 Environment Settings
# ========================
ENVIRONMENT=local
ALLOWED_ORIGINS="*"

# ========================
# ⚙️ Backend Configuration
# ========================
# Supported values: mongo, postgres
AUTH_DB_BACKEND=mongo

# ========================
# 🔐 Authentication (JWT)
# ========================
ACCESS_TOKEN_EXPIRE_MINUTES=20
TOKEN_ISSUER=JANUX-server
TOKEN_AUDIENCE=JANUX-application

# ========================
# 📍 Token Endpoints
# ========================
USER_TOKEN_URL=/auth/login
ADMIN_TOKEN_URL=/auth/login

# ========================
# 🌱 MongoDB Configuration
# ========================
MONGO_DATABASE_NAME=users_db

# ========================
# 🐘 PostgreSQL Configuration
# ========================
POSTGRES_DATABASE_NAME=users_db
POSTGRES_ECHO=false
POSTGRES_POOL_SIZE=5

# ========================
# 🇷 REDIS Configuration
# ========================
REDIS_HOST=redis
REDIS_PORT=6379

# ========================
# 🦄 Uvicorn Configuration
# ========================
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000

```

To use this configuration, copy `.env.example` to `.env`, and modify the values as needed.

!!! tip "Note" 

    **JANUX** accepts `.env` and `.env.local` for development. 
    
    **For production or any other containerized enviroments**, use `.env.<enviroment>` e.g. `.env.test` or `.env.production`.


!!! warning "IMPORTANT"

    Ensure **JANUX_ENCRYPTION_KEY** is a valid **32-byte base64-encoded** string!


## 🔐 Secure Secrets with Docker

For sensitive data, **JANUX** does NOT store credentials in `.env` files but instead loads them from **Docker secrets**. This ensures that sensitive information (e.g., database credentials, encryption keys) is not stored in source code or environment variables.

The expected structure for secrets in local development mimics Docker secrets:

```
📁 secrets/
├── janux_encryption_key
├── jwt_private_key.pem
├── jwt_public_key.pem

# MongoDB (used if AUTH_DB_BACKEND=mongo)
├── mongo_uri
├── mongo_admin_email
├── mongo_admin_password
├── mongo_admin_fullname
├── mongo_admin_role
├── mongo_user_email
├── mongo_user_password
├── mongo_user_fullname
└── mongo_user_role

# PostgreSQL (used if AUTH_DB_BACKEND=postgres)
├── postgres_uri
├── postgres_admin_username
├── postgres_admin_password
├── postgres_admin_fullname
├── postgres_admin_role
├── postgres_user_username
├── postgres_user_password
├── postgres_user_fullname
└── postgres_user_role

```


## 🕵️‍♂️ Setting Up Docker Secrets

If running with Docker Compose, **JANUX** automatically loads secrets from `/run/secrets/`:


➊ To grant execute permissions, run the following command:

```bash
chmod +x ./setup_docker_secret.sh
```

➋ Next, to create these secrets, run the following command in the terminal for MongoDB backend:

```bash
./setup_docker_secret.sh mongo
```

or for PostgreSQL backend: 

```bash
./setup_docker_secret.sh postgres
```


Prior to the deployment, this script will populate **Docker secrets** in `/run/secrets/` by reading from local files.


## 🔄 Loading Secrets in the Application

**JANUX** automatically detects whether it is running:


|Enviroment | Secrets  |
|--- |--- |
| Containerized environment (Docker, Kubernetes) | From `/run/secrets/`|
| Local / development | From `./secrets/` |
| As a fallback | From environment variables |



---

Now that environment variables and secrets are set, continue with **installation**. 🎯
