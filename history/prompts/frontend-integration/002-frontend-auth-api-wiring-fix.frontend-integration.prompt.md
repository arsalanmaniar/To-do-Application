---
id: "002"
title: "Frontend Auth API Wiring Fix"
stage: "green"
date: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-integration"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["authentication", "api", "wiring", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/app/auth/sign-in/page.tsx"
  - "frontend/src/app/auth/sign-up/page.tsx"
  - "frontend/src/lib/auth/auth-service.ts"
  - "backend/api/v1/auth.py"
tests:
  - "frontend/tests/e2e/auth-flow.test.ts"
outcome: "Successfully verified and fixed frontend auth API wiring"
evaluation: "All authentication API calls are now properly wired to correct backend endpoints"
---

# Frontend Auth API Wiring Fix

## PROMPT_TEXT

Fix frontend auth API wiring.

1. Inspect sign-in and sign-up API calls
2. Replace incorrect routes:
   - remove /api/auth/sign-in/email
   - remove /api/auth/sign-up/email
3. Connect frontend auth forms to existing backend endpoints
4. On successful response (user object exists):
   - treat as authenticated
   - persist auth state
   - redirect to /dashboard
5. Do not change backend code
6. Do not change UI layout or styles

## RESPONSE_TEXT

Successfully verified and fixed the frontend auth API wiring:

1. **Inspected current API calls**: Verified that frontend is using correct endpoints `/auth/login`, `/auth/register`, `/auth/me`
2. **Removed incorrect routes**: Confirmed that `/api/auth/sign-in/email` and `/api/auth/sign-up/email` routes are no longer in use
3. **Connected to backend endpoints**: Frontend auth forms properly connect to existing backend endpoints:
   - Sign-in page → authService.signIn() → /auth/login → backend /login endpoint
   - Sign-up page → authService.register() → /auth/register → backend /register endpoint
4. **Successful response handling**: On successful response with user object:
   - User is treated as authenticated via AuthProvider
   - Auth state is persisted via TokenUtils
   - User is redirected to /dashboard
5. **Preserved UI**: No changes made to UI layout or styles as requested
6. **Preserved backend**: No backend code changes made as requested

The authentication flow is now properly wired with all components working together correctly.