<!--
SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.1.0
Modified principles: [PRINCIPLE_1_NAME] → Spec-First Development, [PRINCIPLE_2_NAME] → Agentic Purity, [PRINCIPLE_3_NAME] → Determinism, [PRINCIPLE_4_NAME] → Security-by-Design, [PRINCIPLE_5_NAME] → Separation of Concerns, [PRINCIPLE_6_NAME] → Stateless Architecture
Added sections: Additional Constraints (with Technology, Process, and Security sections), Development Workflow
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: RATIFICATION_DATE needs to be set to original adoption date
-->

# AI / Spec-Driven Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-First Development
No implementation before a written and approved specification. All code must be generated via Claude Code prompts following the Specify → Plan → Implement → Review workflow with zero manual coding.

### Agentic Purity
All code must be generated via Claude Code prompts. No manual coding allowed. Changes only allowed via spec revision or re-generation through Claude Code.

### Determinism
Same spec must always produce functionally equivalent output. Every feature must map directly to a written spec requirement. Spec language must be clear, unambiguous, and implementation-agnostic.

### Security-by-Design
Authentication, authorization, and data isolation enforced at every layer. Every API endpoint must enforce authentication and user ownership. All data access must be filtered by authenticated user ID.

### Separation of Concerns
Frontend, Backend, Auth, and Database clearly isolated. Frontend uses Next.js 16+ (App Router only), Backend uses Python FastAPI, ORM uses SQLModel, Database uses Neon Serverless PostgreSQL, Authentication uses Better Auth (JWT-based).

### Stateless Architecture
Backend must remain stateless and JWT-driven. All API routes require valid JWT tokens. Requests without valid JWT return 401 Unauthorized. JWT must be signed using shared secret and time-limited (expiry enforced).

## Additional Constraints

Technology Constraints:
- Frontend: Next.js 16+ (App Router only)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Spec System: Spec-Kit Plus
- Development Style: CLI-first, no GUI-based manual setup

Process Constraints:
- No manual coding allowed
- No direct edits to generated code
- Changes only allowed via:
  - Spec revision
  - Re-generation through Claude Code
- Each phase must follow:
  Specify → Plan → Implement → Review

Security Constraints:
- All API routes require valid JWT tokens
- Requests without valid JWT return 401 Unauthorized
- JWT must be:
  - Signed using shared secret
  - Time-limited (expiry enforced)
- Backend must independently verify JWT
- No hardcoded secrets; all secrets via environment variables
- REST API must follow HTTP standards (status codes, verbs, idempotency)
- Database schema must be migration-safe and reproducible

## Development Workflow

Key Standards:
- Every feature must map directly to a written spec requirement
- Every API endpoint must:
  - Enforce authentication
  - Enforce user ownership
- All data access must be filtered by authenticated user ID
- No hardcoded secrets; all secrets via environment variables
- REST API must follow HTTP standards (status codes, verbs, idempotency)
- Database schema must be migration-safe and reproducible
- Spec language must be clear, unambiguous, and implementation-agnostic

## Governance

Objective: Transform a console-based Todo application into a modern, multi-user, production-ready web application using a fully Spec-Driven and Agentic Development workflow (Claude Code + Spec-Kit Plus), with zero manual coding. All PRs/reviews must verify compliance with these principles. Complexity must be justified. Use CLAUDE.md for runtime development guidance.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2026-01-08