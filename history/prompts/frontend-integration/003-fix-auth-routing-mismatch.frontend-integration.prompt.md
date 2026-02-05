---
id: "003"
title: "Fix Auth Routing Mismatch"
stage: "green"
date: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-integration"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["routing", "auth", "nextjs", "app-router"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/components/auth/protected-route.tsx"
  - "frontend/src/lib/api/client.ts"
  - "frontend/src/lib/api/interceptors.ts"
  - "frontend/src/components/auth/error-boundary.tsx"
  - "frontend/middleware.ts"
  - "specs/005-frontend-integration/tasks.md"
tests:
  - "frontend/tests/e2e/auth-flow.test.ts"
outcome: "Successfully fixed auth routing mismatch"
evaluation: "All auth redirects now properly use /auth/* prefix"
---

# Fix Next.js App Router Auth Routing Mismatch

## PROMPT_TEXT

Fix Next.js App Router auth routing mismatch.

Auth pages exist under /auth/*
Frontend redirects incorrectly point to /sign-in and /sign-up

Tasks:
1. Update all redirects and links to use /auth/sign-in and /auth/sign-up
2. Do not change backend or API logic
3. Do not move folders
4. Ensure navigation works correctly

## RESPONSE_TEXT

Successfully fixed the Next.js App Router auth routing mismatch:

1. **Updated protected route redirect**: Changed `router.push('/sign-in')` to `router.push('/auth/sign-in')` in `frontend/src/components/auth/protected-route.tsx`
2. **Updated API client redirect**: Changed `window.location.href = '/sign-in'` to `window.location.href = '/auth/sign-in'` in `frontend/src/lib/api/client.ts`
3. **Updated interceptors redirect**: Changed `window.location.href = '/sign-in'` to `window.location.href = '/auth/sign-in'` in `frontend/src/lib/api/interceptors.ts`
4. **Updated error boundary redirect**: Changed `window.location.href = '/sign-in'` to `window.location.href = '/auth/sign-in'` in `frontend/src/components/auth/error-boundary.tsx`
5. **Updated middleware redirect**: Changed `new URL('/sign-in', ...)` to `new URL('/auth/sign-in', ...)` in `frontend/middleware.ts`

All redirects now properly use the /auth/* prefix to match the actual page locations at /auth/sign-in and /auth/sign-up. No backend or API logic was changed, and no folders were moved. Navigation now works correctly.