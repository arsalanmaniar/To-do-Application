# Quickstart Guide: Full-Stack Todo Application

## Overview
This guide provides instructions for setting up, developing, and running the full-stack Todo application with Next.js frontend and FastAPI backend.

## Prerequisites
- Node.js 18+ with npm
- Python 3.10+
- PostgreSQL-compatible database (Neon Serverless recommended)
- Git

## Development Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-jwt-key-here-make-sure-it-is-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run the backend:
```bash
cd backend
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-sure-it-is-at-least-32-characters-long
```

Run the frontend:
```bash
cd frontend
npm run dev
```

## Available Scripts

### Backend
- `uvicorn main:app --reload`: Start development server with auto-reload
- `pytest`: Run backend tests
- `alembic upgrade head`: Apply database migrations

### Frontend
- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm test`: Run frontend tests

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile

### Tasks
- `GET /api/v1/tasks` - Get all tasks for user
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PATCH /api/v1/tasks/{id}/complete` - Toggle task completion

## Database Models

### User
- id (UUID)
- email (string)
- hashed_password (string)
- is_active (boolean)
- created_at (timestamp)
- updated_at (timestamp)

### Task
- id (UUID)
- title (string)
- description (string, optional)
- completed (boolean)
- owner_id (foreign key to User)
- created_at (timestamp)
- updated_at (timestamp)

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API base URL
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Auth service URL
- `BETTER_AUTH_SECRET` - Auth secret key

## Troubleshooting

### Common Issues
1. **Port already in use**: Change ports in environment files
2. **Database connection errors**: Verify DATABASE_URL is correct
3. **JWT errors**: Ensure SECRET_KEY is consistent between frontend and backend
4. **CORS errors**: Check backend CORS configuration

### Development Tips
- Use `npm run dev` for frontend hot reloading
- Use `--reload` flag for backend hot reloading
- Database tables are created automatically on startup
- Authentication is required for all task endpoints