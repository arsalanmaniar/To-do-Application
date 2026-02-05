---
id: "004"
title: "Fix Tasks API Endpoint"
stage: "green"
date: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-integration"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["api", "tasks", "routing", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/app/dashboard/page.tsx"
  - "frontend/src/lib/api/task-api.ts"
  - "frontend/src/components/tasks/task-form.tsx"
  - "specs/005-frontend-integration/tasks.md"
tests:
  - "frontend/tests/e2e/task-crud.test.ts"
outcome: "Successfully fixed tasks API endpoint mismatch"
evaluation: "Dashboard now correctly calls backend tasks endpoint"
---

# Fix Dashboard UI Tasks API Endpoint Mismatch

## PROMPT_TEXT

Dashboard UI calls /tasks API which returns 404.

Tasks:
1. Inspect frontend dashboard page.tsx for tasks fetch
2. Match API URL with existing FastAPI backend routes
3. Fix endpoint mismatch
4. Do not change auth logic
5. Ensure tasks request returns 200

## RESPONSE_TEXT

Successfully fixed the tasks API endpoint mismatch:

1. **Updated dashboard page**: Changed direct API call `apiClient.get('/tasks')` to use proper service `getTasks()` function
2. **Fixed task API service**: Updated all endpoints in `task-api.ts` to use correct `/api/v1/tasks` prefix:
   - `get('/tasks')` → `get('/api/v1/tasks')`
   - `get('/tasks/${taskId}')` → `get('/api/v1/tasks/${taskId}')`
   - `post('/tasks')` → `post('/api/v1/tasks')`
   - `put('/tasks/${taskId}')` → `put('/api/v1/tasks/${taskId}')`
   - `delete('/tasks/${taskId}')` → `delete('/api/v1/tasks/${taskId}')`
   - `patch('/tasks/${taskId}/toggle')` → `patch('/api/v1/tasks/${taskId}/complete')` (also fixed endpoint path to match backend)
3. **Updated task form**: Changed direct API call in `task-form.tsx` to use `createTask()` service function
4. **Preserved auth logic**: No changes made to authentication logic as requested
5. **Standardized API usage**: All components now properly use the task-api service instead of direct API calls

The dashboard now correctly calls the backend tasks endpoint at `/api/v1/tasks` which matches the backend route structure, ensuring requests return 200 status.