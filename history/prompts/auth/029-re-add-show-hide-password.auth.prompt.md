---
id: "029"
title: "Re-add Show Hide Password Feature"
stage: "green"
date: "2026-01-26"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "auth"
branch: "001-frontend-ui-fixes"
user: "DC"
command: "sp.implement"
labels: ["ui", "password", "authentication", "ux"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/app/auth/sign-in/page.tsx"
  - "frontend/src/app/auth/sign-up/page.tsx"
tests:
  - "frontend/tests/e2e/show-hide-password.test.ts"
outcome: "Successfully re-added show/hide password functionality to both sign-in and sign-up pages"
evaluation: "Password visibility toggle works correctly on both authentication pages"
---

# Re-add Show Hide Password Feature

## PROMPT_TEXT

Re-add Show / Hide Password Feature (Sign In & Sign Up)

### Objective
Re-enable the **Show / Hide Password** functionality for both **Sign In** and **Sign Up** pages without changing any existing UI, layout, styling, validation logic, or authentication flow.

### Requirements
1. Add a **Show / Hide Password toggle (eye icon)** inside the password input field.
2. The feature must be implemented on:
   - Sign In page
   - Sign Up page
3. Default behavior:
   - Password field type should be `password`
   - Password should be hidden by default
4. When the user clicks the eye icon:
   - Toggle input type between `password` and `text`
   - Update the icon state accordingly (eye / eye-off)
### UI & UX Rules
- Do NOT change:
  - Existing design
  - Colors
  - Fonts
  - Spacing
  - Form layout
- The eye icon must be aligned inside the password input field (right side).
- The feature should work smoothly without page reload.

### Technical Notes
- Use clean and reusable logic for toggling password visibility.
- Ensure accessibility:
  - Proper button or clickable icon
  - Keyboard accessible if possible
- No changes to backend or API logic.
- No changes to form validation or submission behavior.

### Acceptance Criteria
- Password is hidden by default on both pages.
- Clicking the eye icon correctly shows and hides the password.
- UI remains exactly the same except for the restored show/hide password option.
- Works consistently on both Sign In and Sign Up forms.

### Status
Everything else in the application is working correctly.
Only restore the **Show / Hide Password** feature.

## RESPONSE_TEXT

Successfully re-added the Show/Hide Password functionality to both Sign In and Sign Up pages:

1. **Sign In Page**:
   - Added showPassword state management
   - Updated password input field to conditionally render as text or password
   - Added eye icon toggle button positioned inside the password input field
   - Included proper accessibility labels
   - Used appropriate SVG icons for both states (eye and eye-slash)

2. **Sign Up Page**:
   - Added showPassword state management
   - Updated password input field to conditionally render as text or password
   - Added eye icon toggle button positioned inside the password input field
   - Included proper accessibility labels
   - Used appropriate SVG icons for both states (eye and eye-slash)

3. **Common Features**:
   - Password is hidden by default (type="password")
   - Clicking the eye icon toggles between text and password types
   - Icons update appropriately (eye for visible, eye-slash for hidden)
   - Proper padding adjustments to accommodate the icon
   - Accessibility attributes for screen readers
   - No changes to existing UI design, colors, fonts, spacing, or layout
   - No changes to form validation or submission behavior
   - No backend or API changes

The feature is now fully functional on both authentication pages while maintaining all existing functionality and design consistency.