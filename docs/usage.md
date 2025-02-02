# 🚀 Usage Guide

This guide walks you through using the **JANUX Authentication Gateway**, to authenticate users and managing JWT tokens.

Once running, the API is available at:

```bash
http://localhost:8000
```

Check if the service is live:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```


## 🔑 Authenticating Users

➊ Register a New User

To register a new user, send a POST request to /users/register:

```bash
curl -X POST http://localhost:8000/users/register \
     -H "Content-Type: application/json" \
     -d '{
           "email": "test.user@example.com",
           "full_name": "Test User",
           "password": "Passw0rd123!"
         }'
```

Expected response:

```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "test.user@example.com",
  "full_name": "Test User"
}
```

➋ Logging In

To authenticate, send user credentials to /auth/login:

```bash
curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test.user@example.com&password=Passw0rd123!"
```

Successful login response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 🔐 Using JWT Tokens

Once logged in, use the access token for authentication in API requests. Example of calling a protected route:

```bash
curl -X GET http://localhost:8000/protected-endpoint \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🎫 Managing Admin Accounts

➊ Create a Super Admin (First-Time Setup)

To create a super admin account:

```bash
curl -X POST http://localhost:8000/admins/create \
     -H "Content-Type: application/json" \
     -d '{
           "email": "admin@example.com",
           "full_name": "Admin User",
           "password": "SecureAdminPass123!",
           "role": "super_admin"
         }'
```

➋ Logging in as an Admin

Use the same login endpoint /auth/login but with admin credentials.

```bash
curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@example.com&password=SecureAdminPass123!"
```

## 🔄 Refreshing JWT Tokens

If enabled, a refresh token can be used to get a new access token.

```bash
curl -X POST http://localhost:8000/auth/refresh \
     -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

## 📛 Revoking Tokens (Logout)

To invalidate a token and log out:

```bash
curl -X POST http://localhost:8000/auth/logout \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📂 API Documentation

Interactive API documentation is available at:

- [Swagger UI](http://localhost:8000/docs)
- [Redoc UI](http://localhost:8000/redoc)
