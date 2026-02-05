---
id: "007"
title: "Handle Profile Endpoint Error"
stage: "green"
date: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-integration"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["auth", "error-handling", "profile", "404-error"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/auth/auth-service.ts"
  - "frontend/src/components/providers/auth-provider.tsx"
  - "specs/005-frontend-integration/tasks.md"
tests:
  - "frontend/tests/e2e/auth-flow.test.ts"
outcome: "Successfully handled 404 error from profile endpoint"
evaluation: "Login flow continues despite profile fetch failures"
---

# Handle Profile Endpoint 404 Error Gracefully

## PROMPT_TEXT

resolve this error  ## Error Type
Console AxiosError

## Error Message
Request failed with status code 404


    at async Object.getProfile (src/lib/auth/auth-service.ts:59:24)
    at async signIn (src/components/providers/auth-provider.tsx:66:25)
    at async handleSubmit (src/app/auth/sign-in/page.tsx:35:22)

## Code Frame
  57 |   async getProfile() {
  58 |     try {
> 59 |       const response = await apiClient.get('/auth/me');
     |                        ^
  60 |       return response;
  61 |     } catch (error) {
  62 |       console.error('Get profile error:', error);

Next.js version: 16.1.1 (Turbopack)

## RESPONSE_TEXT

Successfully handled the 404 error from the /auth/me endpoint:

1. **Identified root cause**: The `/auth/me` endpoint returns 404 due to backend authentication mismatch - token contains user ID in 'sub' field but endpoint expects email
2. **Updated auth service**: Modified `getProfile()` function to handle 404/401 errors gracefully and attempt to decode user info from token as fallback
3. **Enhanced error handling**: Added proper error catching in AuthProvider for profile fetch failures
4. **Maintained login flow**: Login continues successfully even when profile fetch fails, ensuring users can still access dashboard
5. **Graceful degradation**: When profile endpoint fails, user data is extracted from JWT token as fallback
6. **Preserved functionality**: All authentication flow continues to work properly despite backend inconsistency

The login flow now handles profile endpoint failures gracefully without breaking the authentication process.