# Data Model: Backend Startup and Database Initialization

## Overview
This document describes the data structures and entities involved in the backend startup and database initialization process.

## Key Entities

### Database Connection
**Description**: Represents the connection to the Neon Serverless PostgreSQL database using DATABASE_URL from environment

**Attributes**:
- database_url: String - The connection string for the database
- engine: SQLAlchemy Engine - The database engine instance
- connection_parameters: Object - Additional connection parameters for Neon Serverless

**Relationships**:
- Connects to Database Tables entity
- Used by FastAPI Application entity

### Database Tables
**Description**: The User and Task tables required by the application, created automatically from SQLAlchemy models

**Attributes**:
- user_table_exists: Boolean - Indicates if User table exists
- task_table_exists: Boolean - Indicates if Task table exists
- table_creation_timestamp: DateTime - When tables were created
- table_schema_version: String - Version of the schema

**Relationships**:
- Created by Database Connection entity
- Used by Application Services entity

### FastAPI Application
**Description**: The main FastAPI application instance that handles requests and manages startup events

**Attributes**:
- app_instance: FastAPI - The FastAPI application object
- startup_handlers: Array - Functions to run on application startup
- environment_config: Object - Configuration loaded from environment variables
- status: String - Current status of the application (starting, running, stopped)

**Relationships**:
- Uses Database Connection entity
- Triggers Database Tables creation

### Environment Configuration
**Description**: Configuration loaded from environment variables including database credentials

**Attributes**:
- database_url: String - Database connection string
- better_auth_secret: String - Authentication secret
- algorithm: String - Encryption algorithm (default: "HS256")
- access_token_expire_minutes: Integer - Token expiration time (default: 30)
- db_echo: Boolean - Whether to echo SQL statements (default: False)

**Relationships**:
- Used by FastAPI Application entity
- Used by Database Connection entity

## Entity Relationships Diagram
```
Environment Configuration
         ↓ (Provides database_url)
Database Connection
         ↓ (Creates/Manages)
Database Tables
         ↑ (Used by)
FastAPI Application
```

## Validation Rules
- database_url must be a valid PostgreSQL connection string
- better_auth_secret must be at least 32 characters long
- access_token_expire_minutes must be a positive integer
- db_echo must be a boolean value

## State Transitions
- Database Connection: uninitialized → connecting → connected → ready
- Database Tables: non-existent → creating → created → verified
- FastAPI Application: initializing → starting → running → serving