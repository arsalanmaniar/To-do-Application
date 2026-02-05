# Quickstart Guide: Todo Full-Stack Web Application – Frontend Integration

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to the existing FastAPI backend
- Environment variables configured for backend API URL and auth settings

## Setup Steps

1. **Initialize Next.js project**
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
   ```

2. **Install Better Auth dependencies**
   ```bash
   cd frontend
   npm install better-auth react
   ```

3. **Install additional dependencies**
   ```bash
   npm install @tanstack/react-query axios
   ```

4. **Configure environment variables**
   Create `.env.local` file with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   ```

5. **Start development servers**
   ```bash
   # Start backend
   cd ../backend && uvicorn main:app --reload

   # In new terminal, start frontend
   cd frontend && npm run dev
   ```

## Testing the Setup
- Navigate to http://localhost:3000
- Verify authentication flow works (sign up/sign in)
- Create a test task to verify CRUD operations
- Check that API calls include JWT tokens in headers

## Integration Points
- Frontend communicates with backend via REST API at `/api/v1/tasks/*`
- Authentication handled via Better Auth with JWT tokens
- Protected routes redirect unauthenticated users to sign-in
- All API calls automatically include authentication tokens