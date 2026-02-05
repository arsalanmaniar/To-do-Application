# Data Model: Full-Stack Todo Application Stabilization

## Entity: User
- **Fields**:
  - id: string (unique identifier)
  - email: string (email address for authentication)
  - hashed_password: string (securely hashed password)
  - is_active: boolean (account status)
  - created_at: datetime (account creation timestamp)
  - updated_at: datetime (last update timestamp)
- **Validation**: Email format validation, uniqueness constraint
- **Relationships**: One-to-many with Task entity

## Entity: Task
- **Fields**:
  - id: string (unique identifier)
  - title: string (task title/name)
  - description: string (optional task description)
  - completed: boolean (completion status)
  - owner_id: string (foreign key to User)
  - created_at: datetime (task creation timestamp)
  - updated_at: datetime (last update timestamp)
- **Validation**: Title required, max length constraints
- **State transitions**: Active ↔ Completed (toggle operation)

## Entity: Session (Implicit)
- **Fields**:
  - token: string (JWT token)
  - expires_at: datetime (token expiration time)
  - user_id: string (associated user)
- **Validation**: Token format validation, expiration check
- **Relationships**: One-to-one with User during active session