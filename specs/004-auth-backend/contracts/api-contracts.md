# API Contracts: Authentication Backend

## Overview
This document defines the API contracts for the authentication backend with FastAPI and Neon Serverless PostgreSQL.

## User Registration Endpoint

### POST /auth/register
**Purpose**: Register a new user account

**Request**:
- Method: POST
- Path: /auth/register
- Headers:
  - Content-Type: application/json
- Body:
```json
{
  "email": "string (valid email format)",
  "password": "string (minimum length requirements)"
}
```

**Response**:
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "id": "string (user ID)",
  "email": "string (user email)",
  "is_active": "boolean",
  "created_at": "ISO 8601 datetime string"
}
```

**Error Responses**:
- 422 Unprocessable Entity: Invalid input data (email format, password requirements)
- 409 Conflict: Email already exists

## User Login Endpoint

### POST /auth/login
**Purpose**: Authenticate user and return JWT token

**Request**:
- Method: POST
- Path: /auth/login
- Headers:
  - Content-Type: application/json
- Body:
```json
{
  "email": "string (valid email format)",
  "password": "string (user password)"
}
```

**Response**:
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "access_token": "string (JWT token)",
  "token_type": "string (bearer)",
  "expires_in": "integer (seconds until expiration)"
}
```

**Error Responses**:
- 401 Unauthorized: Invalid email or password
- 422 Unprocessable Entity: Invalid input data

## Protected Endpoint Example

### GET /protected-example
**Purpose**: Example of a protected endpoint that requires JWT authentication

**Request**:
- Method: GET
- Path: /protected-example
- Headers:
  - Authorization: Bearer {JWT_TOKEN}
- Body: None

**Response**:
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "message": "string (success message)",
  "user_id": "string (authenticated user ID)"
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Insufficient permissions

## Common Error Format

All error responses follow this structure:
```json
{
  "detail": "string (error message)"
}
```

## HTTP Status Codes

### Success Responses
- 200: Request successful
- 201: Resource created

### Client Error Responses
- 400: Bad Request (malformed request)
- 401: Unauthorized (authentication required/failed)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 409: Conflict (resource already exists)
- 422: Unprocessable Entity (validation error)

### Server Error Responses
- 500: Internal Server Error
- 503: Service Unavailable

## Security Requirements

### Authentication
- All protected endpoints require JWT token in Authorization header
- Format: `Authorization: Bearer <JWT_TOKEN>`

### Password Security
- Passwords must be hashed using bcrypt before storage
- Plain text passwords should never be returned in responses

### JWT Token Security
- Tokens must have limited expiration time
- Secret key must be stored securely in environment variables
- Tokens must be validated on each protected request

## Request Validation

### Email Validation
- Must be valid email format (e.g., user@example.com)
- Must be unique across all users
- Length limits: 255 characters maximum

### Password Validation
- Minimum length: 8 characters
- Should include a mix of uppercase, lowercase, numbers, and special characters (recommended)
- Must not be returned in any API responses

## Response Consistency

### Timestamp Format
- All datetime fields must be in ISO 8601 format: YYYY-MM-DDTHH:MM:SS.ssssss
- Example: "2026-01-10T18:00:00.000000"

### Field Consistency
- All ID fields should be consistently formatted (UUID or string)
- Boolean fields should be true/false (not 0/1 or "true"/"false")
- String fields should be properly escaped for JSON