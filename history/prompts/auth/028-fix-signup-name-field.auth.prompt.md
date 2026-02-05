---
id: "028"
title: "Fix Sign Up Name Field"
stage: "green"
date: "2026-01-26"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "auth"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["ui", "signup", "input", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/app/auth/sign-up/page.tsx"
tests:
  - "frontend/tests/e2e/signup-inputs.test.ts"
outcome: "Successfully fixed Full Name field to display text correctly"
evaluation: "Name field now shows text instead of password dots"
---

# Fix Sign Up Name Field

## PROMPT_TEXT

Fix Sign Up page input bug.

ISSUE:
On the Sign Up page, the "Full Name" field is behaving like a password input and shows dots (•••••) instead of text.

REQUIREMENTS:
1) Change "Full Name" input field to:
   - type="text"
   - Visible text while typing
   - Proper caret visibility

2) Ensure:
   - Email remains type="email"
   - Password remains type="password"
   - No other field behavior is affected

RULES:
- Do NOT modify backend, API, auth logic, or database
- Do NOT change validation logic
- Only fix UI/input configuration
- Keep existing Tailwind styles intact
- No regressions

OUTPUT:
- Updated Sign Up page code with corrected input types

## RESPONSE_TEXT

Successfully fixed the Sign Up page input bug:

1. **Fixed Full Name field**: Changed the input type from the incorrect `{showPassword ? "text" : "password"}` to `type="text"` so it properly displays text instead of password dots.

2. **Removed unused state**: Removed the unused `showPassword` state variable that was causing the incorrect behavior, as it's not needed for the name field.

3. **Maintained other fields**: Preserved the correct input types for email (`type="email"`) and password (`type="password"`) fields.

4. **Kept existing styles**: Maintained all existing Tailwind styling and appearance while fixing the core functionality.

5. **No regressions**: Ensured no other functionality was affected by the changes.

The Full Name field now correctly displays typed text instead of masking it as password dots.