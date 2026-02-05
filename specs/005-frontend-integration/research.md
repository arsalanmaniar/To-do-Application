# Research Findings: Todo Full-Stack Web Application – Frontend Integration

## Decision: Next.js App Router Implementation
**Rationale**: Next.js 16+ with App Router is the recommended approach for new Next.js applications, providing better performance, improved routing, and server-side rendering capabilities that align with the requirement for a production-ready frontend.

**Alternatives considered**:
- Pages Router (legacy approach, less optimal for new projects)
- Other frameworks like React with Vite or SvelteKit (would not meet constitution requirement for Next.js)

## Decision: Better Auth Integration Strategy
**Rationale**: Better Auth is specifically designed for Next.js applications and provides JWT-based authentication that aligns with the backend's JWT requirements. It offers server-side authentication capabilities that work well with Next.js App Router.

**Alternatives considered**:
- NextAuth.js (another popular Next.js auth solution, but Better Auth is more modern)
- Auth0/other external providers (would add external dependencies not needed)
- Custom JWT implementation (unnecessary complexity when Better Auth exists)

## Decision: API Client Architecture
**Rationale**: A centralized API client will handle JWT token attachment to all requests, ensuring authentication is managed consistently across the application and meeting the requirement that "API client attaches JWT token to every request".

**Alternatives considered**:
- Direct fetch calls in each component (would lead to code duplication and inconsistent auth handling)
- Multiple API clients (would complicate token management)

## Decision: Protected Routing Implementation
**Rationale**: Next.js App Router middleware provides an effective way to protect routes and redirect unauthenticated users, meeting the requirement for "Protected routes (unauthenticated users redirected)".

**Alternatives considered**:
- Client-side protection only (less secure)
- HOC-based protection (more complex than needed)

## Decision: Task UI Component Architecture
**Rationale**: React components with state management will provide the necessary CRUD functionality for tasks, with proper integration to the backend API for data persistence.

**Alternatives considered**:
- Server components only (would limit interactivity)
- Client components with full SSR (would be overkill for this use case)

## Decision: Backend API Integration Approach
**Rationale**: The frontend will integrate with the existing FastAPI backend using REST API calls with JWT authentication, maintaining the user isolation requirement where "Backend enforces user isolation".

**Alternatives considered**:
- GraphQL instead of REST (not specified in requirements, REST is simpler)
- Separate authentication service (unnecessary complexity when JWT is already established)