# Todo API Backend

A secure, stateless backend API for a multi-user Todo application using FastAPI, SQLModel, and Neon PostgreSQL.

## Overview

This backend provides a RESTful API for managing user tasks with strict data isolation enforced through JWT authentication. The backend independently verifies user identity and ensures tasks are only accessible by their owners.

## Features

- Secure JWT-based authentication and authorization
- Multi-user task management with data isolation
- Full CRUD operations for tasks
- Filtering and pagination support
- RESTful API design
- PostgreSQL database with SQLModel ORM

## API Endpoints

### Task Management

- `GET /api/v1/{user_id}/tasks` - Retrieve all tasks for a user
- `POST /api/v1/{user_id}/tasks` - Create a new task
- `GET /api/v1/{user_id}/tasks/{task_id}` - Retrieve a specific task
- `PUT /api/v1/{user_id}/tasks/{task_id}` - Update a task completely
- `PATCH /api/v1/{user_id}/tasks/{task_id}` - Partially update a task
- `PATCH /api/v1/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/v1/{user_id}/tasks/{task_id}` - Delete a task

## Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

The user_id in the URL must match the user_id in the JWT token.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and JWT secret
   ```

3. Run the application:
   ```bash
   uvicorn backend.main:app --reload
   ```

## Testing

Run tests with pytest:
```bash
pytest
```

## CLI Commands

The backend provides CLI commands for database verification and management:

1. Check database connection:
   ```bash
   python -m backend.cli check-db-connection
   ```

2. List database tables:
   ```bash
   python -m backend.cli list-tables
   ```

3. Check specific tables:
   ```bash
   python -m backend.cli check-tables
   ```

## Database Initialization

The application automatically creates database tables on startup. When the application starts:
1. It loads the DATABASE_URL from environment variables
2. Creates the SQLModel engine for Neon Serverless PostgreSQL
3. Runs `SQLModel.metadata.create_all()` to create tables if they don't exist
4. Logs "Creating database tables..." during the process

## Database Migrations

This project uses Alembic for database migrations. To create and run migrations:

1. Create a new migration:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT secret key for token verification
- `DB_ECHO`: Set to "True" to log SQL queries (default: False)