# Quickstart Guide: Authentication Backend

## Overview
This guide explains how to set up, configure, and use the authentication backend with FastAPI and Neon Serverless PostgreSQL.

## Prerequisites
- Python 3.11+
- pip package manager
- Access to Neon Serverless PostgreSQL database
- uvicorn ASGI server

## Setup Instructions

### 1. Environment Configuration
Create a `.env` file in the project root with the following variables:
```bash
DATABASE_URL=your_neon_database_connection_string
SECRET_KEY=your_jwt_secret_key_at_least_32_characters_long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Install Dependencies
From the project root directory:
```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary passlib[bcrypt] python-jose[cryptography] python-dotenv
```

### 3. Initialize Database
Run the following commands to set up the database:
```bash
# Initialize alembic if not already done
alembic init alembic

# Generate the initial migration
alembic revision --autogenerate -m "Create user table"

# Apply the migration to create tables
alembic upgrade head
```

## Running the Backend

### Start the Application
Run the following command from the project root:
```bash
uvicorn backend.main:app --reload
```

The application will start on http://127.0.0.1:8000

## API Usage

### Register a New User
Register a new user account:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Login to Get JWT Token
Authenticate and receive a JWT token:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Use JWT Token for Protected Endpoints
Access protected resources with the JWT token:
```bash
curl -X GET http://localhost:8000/protected-endpoint \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Database Management

### Running Migrations
Apply all pending migrations:
```bash
alembic upgrade head
```

### Creating New Migrations
After modifying models, create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Downgrade Migrations
Rollback to a previous migration:
```bash
alembic downgrade -1  # Go back one migration
alembic downgrade <migration_id>  # Go back to specific migration
```

## Verification

### Check Database Tables
Verify that the user table was created:
```bash
# Using psql or your preferred PostgreSQL client
psql -d your_database_url -c "\dt"
```

### Test Authentication Flow
1. Register a new user
2. Login to receive a JWT token
3. Use the token to access protected endpoints

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Solution: Verify DATABASE_URL in environment variables
   - Check Neon database connection settings

2. **Alembic Migration Error**
   - Solution: Ensure alembic is properly configured
   - Check that models match the expected database structure

3. **JWT Token Invalid**
   - Solution: Verify SECRET_KEY matches between token generation and verification
   - Check that the token hasn't expired

### Health Check
Visit `http://localhost:8000/docs` to access the interactive API documentation.

## Next Steps
- Implement protected API endpoints that use the JWT token dependency
- Add user profile management endpoints
- Implement password reset functionality
- Add rate limiting to authentication endpoints