---
id: "022"
title: "Fix Task UUID Error"
stage: "green"
date: "2026-01-26"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-integration"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["task", "uuid", "sqlmodel", "database"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "backend/app/services/task_service.py"
tests:
  - "frontend/tests/e2e/task-crud.test.ts"
outcome: "Successfully fixed task API 500 errors caused by UUID conversion issues"
evaluation: "Task CRUD operations now work properly with UUID IDs in SQLite database"
---

# Fix Task UUID Error

## PROMPT_TEXT

Fix the task API 500 errors showing `(builtins.AttributeError) 'str' object has no attribute 'hex'` when performing operations like PATCH /api/v1/tasks/{id}/complete and PUT /api/v1/tasks/{id}. This error occurs when the system tries to query the database using a string ID (UUID) but encounters UUID conversion issues.

## RESPONSE_TEXT

Successfully fixed the UUID conversion error in task service:

1. **Root cause identified**: The Task model uses UUID for the ID field, but the task service methods were passing string IDs directly to `session.get(Task, task_id)`, causing the `'str' object has no attribute 'hex'` error when SQLModel tried to convert the string internally.

2. **Solution implemented**: Updated all task service methods (`get_task_by_id`, `update_task`, `delete_task`, `toggle_task_completion`) to convert string IDs to UUID objects using `UUID(task_id)` before passing to database queries.

3. **Methods updated**:
   - Added `from uuid import UUID` import in each method
   - Convert string ID to UUID object: `uuid_obj = UUID(task_id) if isinstance(task_id, str) and task_id else task_id`
   - Pass UUID object to `session.get(Task, uuid_obj)` instead of raw string

4. **Verification**: Task CRUD operations (create, read, update, delete, toggle completion) now work properly with UUID IDs in the SQLite database without 500 errors.

The task APIs now function correctly with proper UUID handling.