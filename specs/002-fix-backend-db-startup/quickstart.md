# Quickstart Guide: Backend Startup and Database Initialization

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
BETTER_AUTH_SECRET=your_jwt_secret_key
```

### 2. Install Dependencies
From the project root directory:
```bash
pip install fastapi uvicorn sqlmodel pydantic-settings
```

### 3. Verify Backend Structure
Ensure the following files exist:
- `backend/main.py` - Main FastAPI application
- `backend/__init__.py` - Python package marker

## Starting the Backend

### Start the Application
Run the following command from the project root:
```bash
uvicorn backend.main:app --reload
```

The application will:
1. Load configuration from environment variables
2. Create database connection
3. Automatically create database tables if they don't exist
4. Start the FastAPI server

### Expected Output
When the application starts successfully, you should see:
- Log message "Creating database tables..." during startup
- Server listening on http://127.0.0.1:8000
- No ModuleNotFoundError or import errors

## Database Verification

### CLI Commands
The system provides CLI commands to verify database connectivity:

1. Check database connection:
```bash
# Command to be implemented
python -m backend.cli check-db-connection
```

2. Verify table existence:
```bash
# Command to be implemented
python -m backend.cli list-tables
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'app'**
   - Solution: Ensure backend/main.py is properly structured as a self-contained module
   - Verify backend/__init__.py exists

2. **Database Connection Failure**
   - Solution: Check DATABASE_URL in environment variables
   - Verify network connectivity to Neon database

3. **Table Creation Failure**
   - Solution: Ensure database credentials have table creation permissions
   - Check database connection string format

### Health Check
Visit `http://localhost:8000/health` to verify the application is running correctly.

## Next Steps
- Implement API endpoints for user and task management
- Add authentication middleware
- Set up automated testing