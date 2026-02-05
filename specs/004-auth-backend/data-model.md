# Data Model: Authentication Backend

## Overview
This document describes the data structures and entities involved in the authentication backend system.

## Key Entities

### User
**Description**: Represents a registered user in the system with authentication credentials

**Attributes**:
- id: UUID/String - Unique identifier for the user
- email: String - User's email address (unique)
- hashed_password: String - Securely hashed password using bcrypt
- is_active: Boolean - Whether the account is active (default: true)
- created_at: DateTime - Timestamp when the account was created

**Relationships**:
- Related to authentication tokens (via JWT)
- May relate to other user-specific data in the future

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- is_active defaults to true
- created_at defaults to current timestamp

### JWT Token
**Description**: JSON Web Token used for authentication and authorization

**Attributes**:
- sub: String - Subject (user identifier)
- exp: Integer - Expiration timestamp
- iat: Integer - Issued at timestamp
- token_type: String - Token type (usually "access")

**Relationships**:
- Belongs to a User entity
- Used for authentication in API requests

### Authentication Credentials
**Description**: Input data for authentication operations

**Attributes**:
- email: String - User's email address
- password: String - Plain text password (to be hashed)

**Validation Rules**:
- Email must be valid email format
- Password must meet minimum length requirements

## Entity Relationships Diagram
```
Authentication Credentials (email, password)
         ↓ (validation)
User (id, email, hashed_password, is_active, created_at)
         ↑ (JWT generation)
JWT Token (sub, exp, iat, token_type)
```

## State Transitions
- User: inactive → active (after registration/verification)
- User: active → inactive (account deactivation)
- JWT Token: valid → expired (based on expiration time)

## Security Considerations
- Passwords must be hashed using bcrypt before storage
- JWT tokens must have limited expiration time
- User email must be validated for uniqueness
- Authentication attempts should be rate-limited