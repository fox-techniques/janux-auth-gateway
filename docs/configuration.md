# 🔧 Configuration 

???+ info

    Set configuration before installation.

## ⚙️ Environment Variables

**JANUX** uses environment variables for configuration. You can set these using a .env file or system environment variables.

➊ Create a .env File (Recommended for Local Development)

Create a .env file in the project root:

```bash title=".env"
# ========================
# 🌍 Environment Settings
# ========================
ENVIRONMENT=local
CONTAINER=True
ALLOWED_ORIGINS="*"

# ========================
# 🔒 AES Encryption Settings
# ========================
# Encryption settings for the key pair encryption
JANUX_ENCRYPTION_KEY="your_generated_openssl_base64_32character_key"

# ========================
# 🔐 Authentication (JWT)
# ========================
# Paths to private/public keys (used for RS256 JWT signing)
AUTH_PRIVATE_KEY_PATH=keys/private.pem
AUTH_PUBLIC_KEY_PATH=keys/public.pem

# Token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES=20

# Token issuer and audience
TOKEN_ISSUER=JANUX-server
TOKEN_AUDIENCE=JANUX-application

# ========================
# 📍 Token Endpoints
# ========================
USER_TOKEN_URL=/auth/login
ADMIN_TOKEN_URL=/auth/login

# ========================
# 🗄️ Database Configuration
# ========================
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE_NAME=users_db

# Initial user and admin account 
MONGO_INIT_ADMIN_EMAIL=super.admin@example.com
MONGO_INIT_ADMIN_PASSWORD=SuperAdminPassw0rd123!
MONGO_INIT_ADMIN_FULLNAME="Super Adminovski"
MONGO_INIT_ADMIN_ROLE=super_admin

MONGO_INIT_USER_EMAIL=test.user@example.com
MONGO_INIT_USER_PASSWORD=TestUserPassw0rd123!
MONGO_INIT_USER_FULLNAME="Test Userovski"
MONGO_INIT_USER_ROLE=user

# ========================
# 🇷 REDIS Configuration
# ========================
REDIS_HOST=localhost
REDIS_PORT=6379
```

???+ warning

    Ensure JANUX_ENCRYPTION_KEY is a valid 32-byte base64-encoded string!


➋ Set Environment Variables via CLI (For Production & Docker)


=== "Linux/macOS"
  
    ```bash
    export ENVIRONMENT=production
    export MONGO_URI="mongodb://mongodb:27017/janux"
    export REDIS_HOST=redis
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:ENVIRONMENT="production"
    $env:MONGO_URI="mongodb://mongodb:27017/janux"
    $env:REDIS_HOST="redis"
    ```

Now that environment variables are set, continue with **installation**. 🎯
