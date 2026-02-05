# API Contract: Task Management Endpoints

## Base URL
`/api/v1/{user_id}/tasks`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```
The user_id in the URL must match the user_id in the JWT token.

## Endpoints

### GET /api/v1/{user_id}/tasks
**Description**: Retrieve all tasks for the specified user

#### Request
- Method: GET
- Path: `/api/v1/{user_id}/tasks`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Query Parameters:
  - `completed` (optional): Filter by completion status (true/false)
  - `limit` (optional): Maximum number of results (default: 50, max: 100)
  - `offset` (optional): Number of results to skip (default: 0)

#### Response
- Success: 200 OK
- Body:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "string",
      "description": "string or null",
      "completed": true,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ],
  "total": 15,
  "limit": 50,
  "offset": 0
}
```

#### Error Responses
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (JWT user_id doesn't match URL user_id)
- 404: Not Found (user_id doesn't exist)

---

### POST /api/v1/{user_id}/tasks
**Description**: Create a new task for the specified user

#### Request
- Method: POST
- Path: `/api/v1/{user_id}/tasks`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body:
```json
{
  "title": "string (1-255 chars)",
  "description": "string or null (0-2000 chars)",
  "completed": false
}
```

#### Response
- Success: 201 Created
- Body:
```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string or null",
  "completed": false,
  "owner_id": "user-id-from-jwt",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Error Responses
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (JWT user_id doesn't match URL user_id)

---

### GET /api/v1/{user_id}/tasks/{task_id}
**Description**: Retrieve a specific task by ID

#### Request
- Method: GET
- Path: `/api/v1/{user_id}/tasks/{task_id}`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`

#### Response
- Success: 200 OK
- Body:
```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string or null",
  "completed": true,
  "owner_id": "user-id-from-jwt",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Error Responses
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (JWT user_id doesn't match URL user_id)
- 404: Not Found (task doesn't exist or doesn't belong to user)

---

### PUT /api/v1/{user_id}/tasks/{task_id}
**Description**: Update a specific task completely

#### Request
- Method: PUT
- Path: `/api/v1/{user_id}/tasks/{task_id}`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body:
```json
{
  "title": "string (1-255 chars)",
  "description": "string or null (0-2000 chars)",
  "completed": true
}
```

#### Response
- Success: 200 OK
- Body:
```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string or null",
  "completed": true,
  "owner_id": "user-id-from-jwt",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Error Responses
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (JWT user_id doesn't match URL user_id)
- 404: Not Found (task doesn't exist or doesn't belong to user)

---

### PATCH /api/v1/{user_id}/tasks/{task_id}
**Description**: Partially update a specific task

#### Request
- Method: PATCH
- Path: `/api/v1/{user_id}/tasks/{task_id}`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body (any combination of these fields):
```json
{
  "title": "string (1-255 chars)",
  "description": "string or null (0-2000 chars)",
  "completed": true
}
```

#### Response
- Success: 200 OK
- Body:
```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string or null",
  "completed": true,
  "owner_id": "user-id-from-jwt",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Error Responses
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (JWT user_id doesn't match URL user_id)
- 404: Not Found (task doesn't exist or doesn't belong to user)

---

### PATCH /api/v1/{user_id}/tasks/{task_id}/complete
**Description**: Toggle the completion status of a task

#### Request
- Method: PATCH
- Path: `/api/v1/{user_id}/tasks/{task_id}/complete`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body:
```json
{
  "completed": true
}
```

#### Response
- Success: 200 OK
- Body:
```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string or null",
  "completed": true,
  "owner_id": "user-id-from-jwt",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Error Responses
- 400: Bad Request (invalid completed value)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (JWT user_id doesn't match URL user_id)
- 404: Not Found (task doesn't exist or doesn't belong to user)

---

### DELETE /api/v1/{user_id}/tasks/{task_id}
**Description**: Delete a specific task

#### Request
- Method: DELETE
- Path: `/api/v1/{user_id}/tasks/{task_id}`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`

#### Response
- Success: 204 No Content

#### Error Responses
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (JWT user_id doesn't match URL user_id)
- 404: Not Found (task doesn't exist or doesn't belong to user)