# Data Model: Backend API & Data Layer for Multi-User Todo Web Application

**Date**: 2026-01-08

## Overview
This document defines the data models for the secure, stateless backend API for a multi-user Todo application. The models are designed to support user-level data isolation and efficient querying.

## Entity Definitions

### User Entity
**Purpose**: Represents a registered user in the system, identified by external JWT claims

**Attributes**:
- `id`: String/UUID (Primary Key)
  - Source: Extracted from JWT token
  - Constraints: Unique, Not Null
  - Format: Matches Better Auth user ID format
- `email`: String
  - Constraints: Not Null
  - Format: Valid email address
- `created_at`: DateTime
  - Constraints: Not Null
  - Format: ISO 8601 timestamp
  - Default: Current timestamp on creation

**Relationships**:
- One-to-Many: User → Tasks (via owner_id foreign key)

### Task Entity
**Purpose**: Represents a user's todo item with status tracking

**Attributes**:
- `id`: UUID (Primary Key)
  - Constraints: Unique, Not Null
  - Format: Universally unique identifier
  - Default: Auto-generated UUID
- `title`: String
  - Constraints: Not Null
  - Length: 1-255 characters
- `description`: String (Optional)
  - Constraints: Nullable
  - Length: 0-2000 characters
- `completed`: Boolean
  - Constraints: Not Null
  - Default: False
- `owner_id`: String/UUID (Foreign Key)
  - Constraints: Not Null
  - References: User.id
  - Cascade: Delete tasks when user is removed
- `created_at`: DateTime
  - Constraints: Not Null
  - Format: ISO 8601 timestamp
  - Default: Current timestamp on creation
- `updated_at`: DateTime
  - Constraints: Not Null
  - Format: ISO 8601 timestamp
  - Default: Current timestamp on creation and update

**Relationships**:
- Many-to-One: Task → User (via owner_id foreign key)

## Database Constraints

### Primary Keys
- All entities have a unique primary key
- User.id sourced from JWT for consistency with authentication system
- Task.id auto-generated for uniqueness

### Foreign Keys
- Task.owner_id references User.id
- ON DELETE CASCADE: When a user is removed, their tasks are automatically deleted
- ON UPDATE CASCADE: If user ID changes (unlikely), task references update automatically

### Indexes
- Index on User.id (Primary Key)
- Index on Task.owner_id (Foreign Key for efficient user-specific queries)
- Index on Task.created_at (For chronological sorting)
- Composite index on (Task.owner_id, Task.created_at) for efficient user timeline queries

## Validation Rules

### User Validation
- Email must be a valid email format
- ID must match expected JWT claim format
- No duplicate users with same ID

### Task Validation
- Title must be 1-255 characters
- Owner ID must correspond to an existing user
- Completed status must be boolean
- Description limited to 2000 characters if provided

## State Transitions

### Task State Transitions
- `created` → `active`: Task is created with completed=False
- `active` → `completed`: Task completed=True
- `completed` → `active`: Task completed=False (reopened)
- `any_state` → `deleted`: Task is deleted (removed from database)

## Data Access Patterns

### Common Queries
1. Retrieve all tasks for a specific user (filtered by owner_id)
2. Retrieve a specific task by ID (with user ownership verification)
3. Create a new task for a specific user
4. Update task properties (title, description, completed status)
5. Delete a specific task (with ownership verification)

### Security Considerations
- All queries must be filtered by owner_id to ensure data isolation
- Direct access to tasks without user context should be prevented
- Cross-user data access must be blocked at the application level

## Schema Evolution
- Support for soft deletes (adding deleted_at timestamp) in future versions
- Potential addition of categories/tags to tasks in future versions
- Possible addition of due dates and priority levels in future versions