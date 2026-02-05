# Data Model: Todo Full-Stack Web Application – Frontend Integration

## Entity: User
- **Fields**:
  - id: string (unique identifier)
  - email: string (email address for authentication)
  - createdAt: datetime (account creation timestamp)
  - updatedAt: datetime (last update timestamp)
- **Validation**: Email format validation, uniqueness constraint
- **Relationships**: One-to-many with Task entity

## Entity: Task
- **Fields**:
  - id: string (unique identifier)
  - title: string (task title/name)
  - description: string (optional task description)
  - completed: boolean (completion status)
  - userId: string (foreign key to User)
  - createdAt: datetime (task creation timestamp)
  - updatedAt: datetime (last update timestamp)
- **Validation**: Title required, max length constraints
- **State transitions**: Active ↔ Completed (toggle operation)

## Entity: Authentication Session
- **Fields**:
  - token: string (JWT token)
  - expiresAt: datetime (token expiration time)
  - userId: string (associated user)
- **Validation**: Token format validation, expiration check
- **Relationships**: One-to-one with User during active session