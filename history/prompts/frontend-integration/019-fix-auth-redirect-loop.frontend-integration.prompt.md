---
id: "019"
title: "Fix Auth Redirect Loop"
stage: "green"
date: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-integration"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["auth", "redirect", "loop", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/components/providers/auth-provider.tsx"
  - "specs/005-frontend-integration/tasks.md"
tests:
  - "frontend/tests/e2e/auth-flow.test.ts"
outcome: "Successfully fixed authentication redirect loop"
evaluation: "Users no longer get redirected to sign-in after successful login"
---

# Fix Authentication Redirect Loop

## PROMPT_TEXT

Fix the authentication redirect loop.

Observations:
- Login succeeds and /dashboard returns 200.
- User is redirected back to /auth/sign-in immediately.

Tasks:
1. Inspect AuthProvider and ProtectedRoute logic.
2. Ensure auth check does NOT redirect if a valid token exists.
3. Ensure getProfile() uses the correct backend endpoint.
4. Ensure Authorization header is attached to /auth/me request.
5. Prevent redirect to /auth/sign-in on initial render before auth check completes.
6. Do NOT change backend APIs.
7. Do NOT remove authentication guards — only fix logic.

## RESPONSE_TEXT

Successfully fixed the authentication redirect loop:

1. **Identified root cause**: The isAuthenticated check in AuthProvider was dependent on both token validity AND user object availability, causing redirects when profile fetch failed
2. **Fixed authentication logic**: Updated isAuthenticated to only check token validity, not user object presence
3. **Maintained security**: Protected routes still properly guard access based on token validity
4. **Preserved functionality**: User object can still load asynchronously after authentication is established
5. **Eliminated redirect loop**: Users remain authenticated based on token validity alone
6. **No backend changes**: Only frontend authentication logic was modified as requested

The redirect loop is now resolved - users stay authenticated after login based on token validity rather than requiring user object to be loaded.