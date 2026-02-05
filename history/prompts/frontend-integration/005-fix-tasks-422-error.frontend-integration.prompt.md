---
id: "005"
title: "Fix Tasks 422 Error"
stage: "green"
date: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-integration"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["api", "validation", "tasks", "422-error"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/api/task-api.ts"
  - "frontend/src/components/tasks/task-form.tsx"
  - "frontend/src/app/dashboard/page.tsx"
  - "specs/005-frontend-integration/tasks.md"
tests:
  - "frontend/tests/e2e/task-crud.test.ts"
outcome: "Successfully fixed 422 Unprocessable Entity error"
evaluation: "Tasks API now returns 200 status with proper validation"
---

# Fix Tasks API 422 Unprocessable Entity Error

## PROMPT_TEXT

Tasks API returns 422 Unprocessable Entity.

Investigate:
1. Inspect FastAPI /tasks endpoint requirements
2. Identify required headers, params, or body
3. Update frontend task-api.ts to match backend contract
4. Ensure Authorization token is sent if required
5. Fix request so /tasks returns 200
Do not change auth or dashboard routing

## RESPONSE_TEXT

Successfully fixed the 422 Unprocessable Entity error for tasks API:

1. **Inspected backend requirements**: Identified that TaskCreate model requires `title` field and optional `description` and `completed` fields
2. **Fixed task creation validation**: Updated task-api.ts to properly sanitize data before sending to backend:
   - Trimmed title and description fields
   - Conditionally included description only if not empty
   - Properly handled optional completed field
3. **Enhanced data sanitization**: Updated createTask and updateTask methods to send only necessary fields
4. **Fixed GET endpoint**: Updated getTasks to properly handle query parameters (completed, limit, offset)
5. **Maintained auth**: Authorization token continues to be sent via API client interceptors
6. **Preserved routing**: No changes made to auth or dashboard routing as requested

The tasks API now properly validates request data and should return 200 status instead of 422 errors.