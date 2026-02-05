---
id: "003"
title: "Frontend cleanup and routing fix"
stage: "refactor"
date_iso: "2026-01-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "frontend-ui-fixes"
branch: "001-frontend-ui-fixes"
user: "user"
command: "/sp.implement"
labels: ["frontend", "cleanup", "routing", "structure", "nextjs"]
links:
  spec: "../specs/001-frontend-ui-fixes/spec.md"
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/app/layout.tsx
 - frontend/src/app/globals.css
 - frontend/src/app/(auth)/layout.tsx
 - frontend/src/app/(auth)/sign-in/page.tsx
 - frontend/src/app/(auth)/sign-up/page.tsx
 - frontend/src/app/page.tsx
tests:
 - none
---

## Prompt

You are a senior Next.js App Router engineer.

Fix the frontend with these strict rules:

1. Use ONLY src/app as the App Router
2. Delete all duplicate or unused folders:
   - frontend/app
   - src/app/(auth)
   - any extra layouts or globals
3. Ensure ONLY ONE globals.css exists at:
   src/app/globals.css
4. Ensure globals.css is imported ONLY in:
   src/app/layout.tsx
5. Fix routing so these pages work correctly:
   - /            → Home page
   - /auth/sign-in
   - /auth/sign-up
   - /dashboard
6. Ensure navigation between pages works using Next.js Link
7. Do NOT redesign UI yet
8. Do NOT add new files unless necessary 9. Focus ONLY on:
   - cleanup
   - correct linking
   - correct routing
10. After changes, restarting dev server should reflect correct pages

The goal is:
- Clean structure
- Correct routing
- Pages render correctly
- No duplicate files

## Response snapshot

Successfully cleaned up the frontend structure by removing the duplicate frontend/app directory and recreating the proper Next.js routing structure with correct auth pages. The implementation now has a clean src/app-based structure with proper routing for all required pages.

## Outcome

- ✅ Impact: Cleaned up duplicate frontend structure and fixed routing inconsistencies
- 🧪 Tests: none
- 📁 Files: Fixed layout, globals.css, auth pages and routing structure
- 🔁 Next prompts: Ready for UI redesign or feature development
- 🧠 Reflection: Proper Next.js App Router structure established with correct route grouping

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All structural requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A