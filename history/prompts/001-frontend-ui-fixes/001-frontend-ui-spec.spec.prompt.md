---
id: "001"
title: "Frontend UI fixes spec"
stage: "spec"
date_iso: "2026-01-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-ui-fixes"
branch: "001-frontend-ui-fixes"
user: "user"
command: "/sp.specify"
labels: ["frontend", "ui", "styling", "tailwind", "specification"]
links:
  spec: "../specs/001-frontend-ui-fixes/spec.md"
  ticket: null
  adr: null
  pr: null
files:
 - ../specs/001-frontend-ui-fixes/spec.md
 - ../specs/001-frontend-ui-fixes/checklists/requirements.md
tests:
 - none
---

## Prompt

You are a senior Next.js + Tailwind architect.

Project context:
- Next.js App Router
- TypeScript
- Tailwind CSS already installed
- Current issue: Tailwind styles not applying, duplicate app routers, broken auth routing, poor UI

Your tasks:

1. Use ONLY src/app as the App Router
2. Remove any legacy or duplicate routing assumptions
3. Ensure globals.css is correctly imported in src/app/layout.tsx
4. Verify Tailwind directives exist in globals.css:
   @tailwind base;
   @tailwind components;
   @tailwind utilities;

5. Fix routing so the application flow is:
   - /            → Home page
   - /auth/sign-in
   - /auth/sign-up
   - /dashboard   (protected later)

6. Build a clean HOME PAGE UI:
   - Top navigation bar
   - Logo on left
   - Sign In & Sign Up buttons on right
   - Modern Tailwind styling
   - Responsive layout7. Build AUTH UI:
   - Centered card layout
   - Email + password fields
   - Proper Tailwind styling
   - No raw HTML default styles
   - Error and loading states

8. Improve overall UI quality:
   - Consistent spacing
   - Modern fonts
   - Proper buttons
   - Tailwind utility usage

9. Do NOT add new frameworks
10. Do NOT change backend logic
11. Only improve frontend structure and UI

After changes:
- The UI must visibly change
- Tailwind must be clearly working
- No duplicate folders
- Clean production-grade structure

## Response snapshot

Created comprehensive feature specification for frontend UI fixes and Tailwind styling improvements, including user scenarios, functional requirements, and success criteria.

## Outcome

- ✅ Impact: Complete specification document created with user scenarios, requirements, and success criteria for frontend UI improvements
- 🧪 Tests: none
- 📁 Files: ../specs/001-frontend-ui-fixes/spec.md, ../specs/001-frontend-ui-fixes/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Clear separation of concerns in specification helps ensure frontend-only changes without backend modifications

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A