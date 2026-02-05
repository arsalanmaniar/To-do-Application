---
id: "017"
title: "Fix Authentication Infinite Loop"
stage: "green"
date: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-integration"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["auth", "api", "infinite-loop", "401-error", "token-refresh"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/api/client.ts"
  - "frontend/src/lib/auth/token-refresh.ts"
  - "specs/005-frontend-integration/tasks.md"
tests:
  - "frontend/tests/e2e/auth-flow.test.ts"
outcome: "Successfully fixed infinite 401 loop and token persistence issues"
evaluation: "Authentication now works without infinite loops and tokens persist correctly"
---

# Fix Authentication Issues: Infinite 401 Loop and Token Persistence

## PROMPT_TEXT

You are working inside an existing Next.js 16 (App Router) project.
Do NOT refactor unrelated code.
Do NOT change backend APIs, routes, or UI components.

TASK:
Fix authentication issues without breaking any existing functionality.

CURRENT CRITICAL ISSUES (must be addressed):

1) INFINITE 401 LOOP
- Axios client has request/response interceptors.
- On 401, it tries to refresh token and retry requests.
- Backend does NOT support refresh-token flow.
- This causes an infinite login → 401 → retry → redirect loop.

FIX:
- Disable token refresh + retry logic ONLY for 401 responses.
- On 401:
  - Clear auth token from storage
  - Redirect user to /auth/sign-in
  - Prevent retrying the same request again

2) LOGIN STATE NOT PERSISTING
- Login API succeeds and returns a valid JWT.
- Token exists but protected routes still treat user as unauthenticated.
- Root cause: token handling inconsistency.

FIX:
- Ensure a SINGLE token key is used everywhere: "auth-token"
- Ensure token is:
  - saved immediately after successful login
  - read correctly by Axios request interceptor
- Do NOT rename keys or change backend response structure.

IMPLEMENTATION RULES:
- Only update src/lib/api/client.ts and token handling logic if needed
- Do NOT modify pages, components, or backend URLs
- Keep all existing headers, baseURL, and timeout config
- No new libraries
- No breaking changes

FINAL REQUIREMENTS:
- Login should succeed once and stop looping
- Protected routes should work after login
- On real 401 (expired/invalid token), user should be redirected to sign-in once
- No infinite retries
- App should remain stable

After changes:
- Briefly explain what was changed and why (max 5 bullets)

## RESPONSE_TEXT

Successfully resolved both critical authentication issues:

1. **Fixed infinite 401 loop**: Modified the API client response interceptor to immediately clear the token and redirect to sign-in on 401 responses, without attempting token refresh or retrying requests. This eliminates the infinite loop caused by the backend's lack of refresh token support.

2. **Fixed token persistence**: Ensured consistent token handling using the "auth-token" key across all auth utilities. The token is now properly stored after successful login and correctly read by the API request interceptor.

3. **Updated token refresh logic**: Modified the TokenRefresh utility to properly handle the backend's lack of refresh token support by simply validating existing tokens rather than attempting to refresh them.

4. **Preserved existing functionality**: All changes maintain existing API configurations, headers, timeouts, and do not break any existing functionality.

5. **Enhanced error handling**: Improved 401 error handling to immediately redirect users to sign-in page without retry attempts, providing a better user experience.

The authentication system now works properly without infinite loops, tokens persist correctly after login, and users are properly redirected to sign-in on authentication failures.