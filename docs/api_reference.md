# 📖 API Reference

This section documents all available endpoints in **JANUX Authentication Gateway**, covering authentication, user management, admin operations, and system status.

## 🌍 Base Endpoints

Endpoints for general service interaction and health checks.

### 🏠 Welcome Message

Returns a welcome message from the authentication service.

- **Endpoint:** `GET /`
- **Response (Success 200):**
```json
{
  "message": "Welcome to the JANUX Authentication Gateway!"
}
```

### 💚 Health Check

Verify if the service is running and responsive.

- **Endpoint:** `GET /health`
- **Response (Success 200):**
```json
{
"status": "healthy"
}
```

### 🔄 Readiness Probe

Indicates if the application is ready to receive traffic.

- **Endpoint:** `GET /readiness`
- **Response (Success 200):**
```json
{
  "status": "ready"
}
```

### 🚀 Liveness Probe

Checks if the application is alive.

- **Endpoint:** `GET /liveness`
- **Response (Success 200):**
```json
{
  "status": "alive"
}
```

## 🔑 Authentication Endpoints

Handles user and admin authentication, JWT token issuance, and logout.

### 🔐 Login

Authenticate a user or admin and receive an access token.

- **Endpoint:** `POST /auth/login`
- **Request Body (Form Data):**
```json
{
  "username": "user@example.com",
  "password": "SecurePass123!"
}
```
- **Response (Success 200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
```
- **Response (Failure 401 - Unauthorized):**
```json
{
  "detail": "Invalid email or password"
}
```
- **Response (Failure 429 - Too Many Requests):**
```json
{
  "detail": "Too many login attempts. Please try again later."
}
```

## 👤 User Endpoints

Endpoints for user registration, profile management, and logout.

### 📝 Register User

Creates a new user account.

- **Endpoint:** `POST /users/register`
- **Request Body (JSON):**
```json
{
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "password": "SecurePassw0rd123!"
}
```
- **Response (Success 201):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "full_name": "User Name"
}
```
- **Response (Failure 409 - Conflict):**
```json
{
  "detail": "Email already registered."
}
```

- **Response (Failure 429 - Too Many Requests):**
```json
{
  "detail": "Too many requests. Please try again later."
}
```

### 👀 Get Current User Profile

Retrieve details of the authenticated user.

- **Endpoint:** `GET /users/profile`
- **Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

- **Response (Success 200):**
```json
{
  "message": "This is your profile",
  "user": {
    "email": "user@example.com",
    "role": "user"
  }
}
```
- **Response (Failure 401 - Unauthorized):**
```json
{
  "detail": "Could not validate user."
}
```

### 🚪 User Logout

Logs out the currently authenticated user.

- **Endpoint:** `POST /users/logout`
- **Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```
- **Response (Success 200):**
```json
{
  "message": "You have been logged out successfully."
}
```

- **Response (Failure 401 - Unauthorized):**
```json
{
  "detail": "Could not validate user."
}
```

## 🛡️ Admin Endpoints

Endpoints for admin actions like user management and profile retrieval.

### 📋 List All Users

Fetches all registered users (Admin Only).

- **Endpoint:** `GET /admins/users`
- **Headers:**
```http
Authorization: Bearer ADMIN_ACCESS_TOKEN
```
- **Response (Success 200):**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "full_name": "User Name",
    "role": "user"
  },
  {
    "id": "607f1f77bcf86cd799439012",
    "email": "admin@example.com",
    "full_name": "Admin User",
    "role": "admin"
  }
]
```
- **Response (Failure 401 - Unauthorized):**
```json
{
  "detail": "Not enough permissions."
}
```

### ❌ Delete User (Admin Only)

Deletes a user by ID.

- **Endpoint:** `DELETE /admins/users/{user_id}`
- **Headers:**
```http
Authorization: Bearer ADMIN_ACCESS_TOKEN
```
- **Response (Success 200):**
```json
{
  "message": "User ID 507f1f77bcf86cd799439011 successfully deleted."
}
```
- **Response (Failure 404 - Not Found):**
```json
{
  "detail": "User not found."
}
```
- **Response (Failure 401 - Unauthorized):**
```json
{
  "detail": "Not enough permissions."
}
```

### 👤 Get Admin Profile

Retrieve the currently authenticated admin profile.

- **Endpoint:** `GET /admins/profile`
- **Headers:**
```http
Authorization: Bearer ADMIN_ACCESS_TOKEN
```

- **Response (Success 200):**
```json
{
  "message": "This is your admin profile",
  "admin": {
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

### 🚪 Admin Logout

Logs out the currently authenticated admin.

- **Endpoint:** `POST /admins/logout`
- **Headers:**
```http
Authorization: Bearer ADMIN_ACCESS_TOKEN
```

- **Response (Success 200):**
```json
{
  "message": "You have been logged out successfully."
}
```

- **Response (Failure 401 - Unauthorized):**
```json
{
  "detail": "Not enough permissions."
}
```

## 📂 API Documentation

Access interactive API docs:

- [Swagger UI](http://localhost:8000/docs)
- [Redoc UI](http://localhost:8000/redoc)