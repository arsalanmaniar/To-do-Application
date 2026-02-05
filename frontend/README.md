# Todo Full-Stack Web Application - Frontend

This is the frontend component of a full-stack todo application built with Next.js, featuring secure authentication and task management capabilities.

## Features

- 🔐 **Secure Authentication**: User registration and login with JWT-based authentication
- 📝 **Task Management**: Full CRUD operations for todo tasks
- 🔒 **Protected Routes**: Automatic redirection for unauthenticated users
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Performance Optimized**: Fast loading times and smooth interactions
- 🛡️ **Security Focused**: Proper data isolation and secure API communication

## Tech Stack

- **Frontend Framework**: Next.js 16+ with App Router
- **Authentication**: Better Auth
- **State Management**: React Context API
- **Data Fetching**: Axios with interceptors
- **UI Components**: Tailwind CSS
- **API Communication**: REST API with JWT authentication
- **Environment Management**: Environment variables for configuration

## Prerequisites

- Node.js 18+
- npm or yarn
- Access to the backend API server

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hackathon-phase-2/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables by creating a `.env.local` file:
   ```env
   # Backend API Configuration
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

   # Better Auth Configuration
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-sure-it-is-at-least-32-characters-long

   # Database Configuration (if needed)
   DATABASE_URL=postgresql://user:password@localhost:5432/mydb

   # Other Environment Variables
   NODE_ENV=development
   ```

## Running the Application

### Development Mode

```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:3000

### Production Build

```bash
npm run build
npm start
# or
yarn build
yarn start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (auth)/            # Authentication pages
│   │   │   ├── sign-in/       # Sign-in page
│   │   │   └── sign-up/       # Sign-up page
│   │   ├── dashboard/         # User dashboard
│   │   └── layout.tsx         # Global layout
│   ├── components/            # Reusable UI components
│   │   ├── auth/             # Authentication components
│   │   ├── providers/        # Context providers
│   │   ├── tasks/            # Task-related components
│   │   └── ui/               # Generic UI components
│   ├── lib/                  # Library/utility functions
│   │   ├── api/              # API client and services
│   │   └── auth/             # Authentication utilities
└── middleware.ts              # Route protection middleware
```

## Key Components

### Authentication
- **Sign Up Page**: `/src/app/(auth)/sign-up/page.tsx`
- **Sign In Page**: `/src/app/(auth)/sign-in/page.tsx`
- **Auth Provider**: `/src/components/providers/auth-provider.tsx`
- **Protected Route**: `/src/components/auth/protected-route.tsx`

### Task Management
- **Dashboard**: `/src/app/dashboard/page.tsx`
- **Task Form**: `/src/components/tasks/task-form.tsx`
- **Task List**: `/src/components/tasks/task-list.tsx`
- **Task Detail**: `/src/components/tasks/task-detail.tsx`

### API Layer
- **API Client**: `/src/lib/api/client.ts`
- **Auth API**: `/src/lib/api/auth-api.ts`
- **Task API**: `/src/lib/api/task-api.ts`

### Authentication Utilities
- **Token Utils**: `/src/lib/auth/token-utils.ts`
- **Token Refresh**: `/src/lib/auth/token-refresh.ts`
- **Better Auth Client**: `/src/lib/auth/better-auth-client.ts`

## Security Features

- **JWT Token Management**: Automatic token refresh and expiration handling
- **Request Interceptors**: Automatic JWT attachment to all API requests
- **Response Interceptors**: Graceful handling of authentication errors
- **Data Isolation**: User data validation to ensure proper isolation
- **Secure Storage**: Proper token storage and retrieval mechanisms

## API Endpoints Used

The frontend communicates with the backend API for the following operations:

- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile
- `POST /auth/refresh` - Refresh authentication token
- `GET /tasks` - Get user tasks
- `POST /tasks` - Create new task
- `PUT /tasks/:id` - Update task
- `DELETE /tasks/:id` - Delete task
- `PATCH /tasks/:id/toggle` - Toggle task completion

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_BACKEND_URL` | Backend server URL | `http://localhost:8000` |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Better Auth server URL | `http://localhost:3000` |
| `BETTER_AUTH_SECRET` | JWT secret for authentication | `your-super-secret-jwt-key...` |
| `DATABASE_URL` | Database connection string | `postgresql://...` |
| `NODE_ENV` | Environment mode | `development` or `production` |

## Error Handling

The application includes comprehensive error handling:

- **API Errors**: Intercepted and displayed with user-friendly messages
- **Authentication Errors**: Automatic token refresh or redirect to login
- **Network Errors**: Retry logic with exponential backoff
- **User Feedback**: Clear error messages with options to retry or dismiss

## Performance Optimizations

- **Code Splitting**: Automatic by Next.js
- **Image Optimization**: Next.js Image component
- **API Caching**: Intelligent caching strategies
- **Optimistic Updates**: Immediate UI feedback
- **Loading States**: Visual feedback during operations
- **Bundle Optimization**: Tree shaking and minification

## Development Guidelines

### Adding New Components
1. Place reusable components in the appropriate directory under `src/components/`
2. Use TypeScript interfaces for props
3. Follow accessibility best practices
4. Include proper loading and error states

### API Integration
1. Add new endpoints to the appropriate API service file
2. Use the centralized API client for all requests
3. Implement proper error handling
4. Follow consistent response format

### Authentication
1. Wrap protected pages with `ProtectedRoute` component
2. Use the `useAuth` hook for authentication state
3. Implement proper token refresh logic
4. Ensure user data isolation

## Troubleshooting

### Common Issues

**Issue**: Authentication not working
**Solution**: Verify that the backend API is running and environment variables are correctly set

**Issue**: API requests returning 401 errors
**Solution**: Check that JWT tokens are being properly attached to requests and that tokens haven't expired

**Issue**: Protected routes not redirecting
**Solution**: Ensure the middleware is properly configured and the auth provider is wrapping the application

**Issue**: Task operations not working
**Solution**: Verify that the backend API endpoints are accessible and that JWT tokens are valid

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.