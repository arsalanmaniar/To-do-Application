# Quickstart Guide: Backend API & Data Layer for Multi-User Todo Web Application

**Date**: 2026-01-08

## Overview
This guide provides the essential steps to set up, configure, and run the backend API for the multi-user Todo application.

## Prerequisites
- Python 3.11+
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- pip package manager
- Virtual environment tool (venv, conda, etc.)

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development/testing
```

### 4. Environment Configuration
Copy the example environment file:
```bash
cp .env.example .env
```

Configure the following environment variables in `.env`:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-jwt-secret-key-here
```

### 5. Database Setup
Initialize the database:
```bash
# If using Alembic for migrations
alembic upgrade head
```

Alternatively, create tables manually using the SQLModel metadata:
```bash
python -c "from app.database.base import engine; from app.models.user import User; from app.models.task import Task; User.metadata.create_all(engine); Task.metadata.create_all(engine)"
```

## Running the Application

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Usage

### Authentication
All endpoints require a valid JWT token obtained from Better Auth. Include the token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

### Example Requests
Once the server is running, you can test endpoints:

Get all tasks for a user:
```bash
curl -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
     http://localhost:8000/api/v1/user123/tasks
```

Create a new task:
```bash
curl -X POST \
     -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Task", "description": "Task description"}' \
     http://localhost:8000/api/v1/user123/tasks
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Run All Tests
```bash
pytest
```

## Key Components

### Project Structure
```
backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── core/                # Configuration and security
│   ├── models/              # SQLModel database models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── database/            # Database session and engine
│   ├── api/                 # API routes and endpoints
│   └── utils/               # Utility functions
├── tests/                   # Test suite
├── requirements.txt         # Runtime dependencies
└── requirements-dev.txt     # Development dependencies
```

### Main Dependencies
- FastAPI: Web framework with automatic API documentation
- SQLModel: Database ORM with Pydantic integration
- python-jose: JWT token handling
- psycopg2-binary: PostgreSQL adapter
- pytest: Testing framework

## API Endpoints Reference
- `GET /api/v1/{user_id}/tasks` - Get all tasks for user
- `POST /api/v1/{user_id}/tasks` - Create new task
- `GET /api/v1/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/v1/{user_id}/tasks/{task_id}` - Update task completely
- `PATCH /api/v1/{user_id}/tasks/{task_id}` - Partially update task
- `PATCH /api/v1/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/v1/{user_id}/tasks/{task_id}` - Delete task

## Troubleshooting

### Common Issues
- **Database Connection**: Verify DATABASE_URL is correct and database server is running
- **JWT Validation**: Ensure BETTER_AUTH_SECRET matches the one used by Better Auth
- **User ID Mismatch**: Confirm the user_id in JWT matches the one in the URL path

### Enable Debug Logging
Set the LOG_LEVEL environment variable to "debug":
```bash
LOG_LEVEL=debug uvicorn app.main:app --reload
```

## Next Steps
1. Review the API documentation at `/docs` when running
2. Implement authentication integration with Better Auth
3. Add monitoring and logging for production deployment
4. Set up CI/CD pipeline for automated testing and deployment