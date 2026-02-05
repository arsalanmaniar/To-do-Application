# API Contract: Task Management Endpoints

## Base URL
`http://localhost:8000/api/v1` (or as configured in environment)

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Endpoints

### GET /tasks
**Purpose**: Retrieve all tasks for the authenticated user

**Request**:
- Method: GET
- Headers: Authorization: Bearer {jwt_token}
- Query Parameters: None

**Response**:
- Success: 200 OK
- Body: Array of task objects
```json
[
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "owner_id": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```
- Error: 401 Unauthorized (invalid/expired token)

### POST /tasks
**Purpose**: Create a new task for the authenticated user

**Request**:
- Method: POST
- Headers: Authorization: Bearer {jwt_token}, Content-Type: application/json
- Body:
```json
{
  "title": "string",
  "description": "string"
}
```

**Response**:
- Success: 201 Created
- Body:
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "completed": false,
  "owner_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
- Error: 400 Bad Request (validation error), 401 Unauthorized

### GET /tasks/{taskId}
**Purpose**: Retrieve a specific task by ID

**Request**:
- Method: GET
- Headers: Authorization: Bearer {jwt_token}
- Path Parameter: taskId (string)

**Response**:
- Success: 200 OK
- Body: Single task object
- Error: 401 Unauthorized, 404 Not Found (task doesn't exist or belongs to another user)

### PUT /tasks/{taskId}
**Purpose**: Update an existing task

**Request**:
- Method: PUT
- Headers: Authorization: Bearer {jwt_token}, Content-Type: application/json
- Path Parameter: taskId (string)
- Body:
```json
{
  "title": "string",
  "description": "string",
  "completed": "boolean"
}
```

**Response**:
- Success: 200 OK
- Body: Updated task object
- Error: 400 Bad Request, 401 Unauthorized, 404 Not Found

### PATCH /tasks/{taskId}/complete
**Purpose**: Toggle task completion status

**Request**:
- Method: PATCH
- Headers: Authorization: Bearer {jwt_token}
- Path Parameter: taskId (string)

**Response**:
- Success: 200 OK
- Body: Updated task object with toggled completion status
- Error: 401 Unauthorized, 404 Not Found

### DELETE /tasks/{taskId}
**Purpose**: Delete a task

**Request**:
- Method: DELETE
- Headers: Authorization: Bearer {jwt_token}
- Path Parameter: taskId (string)

**Response**:
- Success: 204 No Content
- Error: 401 Unauthorized, 404 Not Found

## Authentication Endpoints

### POST /auth/register
**Purpose**: Register a new user

**Request**:
- Method: POST
- Headers: Content-Type: application/json
- Body:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response**:
- Success: 200 OK
- Body:
```json
{
  "id": "string",
  "email": "string",
  "is_active": true,
  "created_at": "datetime"
}
```

### POST /auth/login
**Purpose**: Authenticate a user

**Request**:
- Method: POST
- Headers: Content-Type: application/json
- Body:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response**:
- Success: 200 OK
- Body:
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

### GET /auth/me
**Purpose**: Get current user's profile

**Request**:
- Method: GET
- Headers: Authorization: Bearer {jwt_token}

**Response**:
- Success: 200 OK
- Body:
```json
{
  "id": "string",
  "email": "string",
  "is_active": true,
  "created_at": "datetime"
}
```