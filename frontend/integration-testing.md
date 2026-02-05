# Integration Testing Guide: Todo Frontend with Backend API

## Overview
This document provides a comprehensive guide for performing final integration testing between the frontend application and the backend API.

## Prerequisites

Before beginning integration testing, ensure:

1. Backend API server is running and accessible
2. Frontend application is built and running
3. Environment variables are properly configured
4. Database is accessible and properly seeded (if needed)

## Pre-Testing Setup

### 1. Environment Configuration
Verify the following environment variables are set correctly:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000  # Or your backend URL
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000  # Or your auth service URL
```

### 2. Backend Health Check
Ensure the backend API is responsive:

```bash
curl -X GET http://localhost:8000/health
# Should return: {"status": "healthy"}
```

## Test Scenarios

### 1. Authentication Flow Testing

#### Test Case 1.1: User Registration
**Objective**: Verify new user can register successfully

**Steps**:
1. Navigate to `/sign-up`
2. Enter valid registration details (name, email, password)
3. Submit the form
4. Verify redirect to dashboard
5. Check that authentication token is stored

**Expected Results**:
- User is registered in the backend
- Authentication token is received and stored
- User is redirected to dashboard
- Auth state is properly set in frontend

#### Test Case 1.2: User Login
**Objective**: Verify existing user can authenticate

**Steps**:
1. Navigate to `/sign-in`
2. Enter valid login credentials
3. Submit the form
4. Verify access to protected routes
5. Check that authentication token is updated

**Expected Results**:
- User is authenticated
- Authentication token is received and stored
- Access to protected routes is granted
- Auth state is properly updated

#### Test Case 1.3: Protected Route Access
**Objective**: Verify unauthenticated users are redirected

**Steps**:
1. Log out of the application
2. Try to access `/dashboard`
3. Verify redirect to `/sign-in`

**Expected Results**:
- Unauthenticated users are redirected to sign-in
- No access to protected routes

### 2. Task Management Testing

#### Test Case 2.1: Create Task
**Objective**: Verify authenticated users can create tasks

**Steps**:
1. Log in to the application
2. Navigate to `/dashboard`
3. Fill in task details in the form
4. Submit the form
5. Verify task appears in the task list

**Expected Results**:
- Task is created in the backend
- Task appears in the frontend task list
- API returns success response
- UI updates immediately

#### Test Case 2.2: Read Tasks
**Objective**: Verify tasks are properly loaded and displayed

**Steps**:
1. Log in to the application
2. Navigate to `/dashboard`
3. Verify existing tasks are loaded
4. Check that only user's tasks are displayed

**Expected Results**:
- User's tasks are loaded from backend
- Only authenticated user's tasks are displayed
- Tasks are properly formatted in the UI

#### Test Case 2.3: Update Task
**Objective**: Verify tasks can be updated

**Steps**:
1. Log in to the application
2. Navigate to `/dashboard`
3. Click "Edit" on an existing task
4. Modify task details
5. Save the changes
6. Verify update in the UI

**Expected Results**:
- Task is updated in the backend
- UI reflects the changes
- API returns success response

#### Test Case 2.4: Toggle Task Completion
**Objective**: Verify task completion status can be toggled

**Steps**:
1. Log in to the application
2. Navigate to `/dashboard`
3. Toggle completion status of a task
4. Verify status change in the UI

**Expected Results**:
- Task completion status is updated in backend
- UI reflects the new status
- API returns success response

#### Test Case 2.5: Delete Task
**Objective**: Verify tasks can be deleted

**Steps**:
1. Log in to the application
2. Navigate to `/dashboard`
3. Click "Delete" on a task
4. Confirm deletion in the modal
5. Verify task is removed from the list

**Expected Results**:
- Task is deleted from the backend
- Task is removed from the frontend list
- API returns success response

### 3. Authentication Token Management

#### Test Case 3.1: Token Attachment
**Objective**: Verify JWT tokens are attached to API requests

**Steps**:
1. Open browser developer tools
2. Navigate to the network tab
3. Perform any authenticated action
4. Inspect API request headers

**Expected Results**:
- `Authorization: Bearer <token>` header is present
- Token is valid and properly formatted

#### Test Case 3.2: Token Expiration Handling
**Objective**: Verify expired tokens are handled gracefully

**Steps**:
1. Manually expire an authentication token
2. Perform an API request
3. Verify automatic token refresh or redirect

**Expected Results**:
- Token refresh is attempted
- If refresh fails, user is redirected to sign-in
- No 401 errors during normal operation

#### Test Case 3.3: Invalid Token Handling
**Objective**: Verify invalid tokens are handled properly

**Steps**:
1. Use an invalid/modified authentication token
2. Perform an API request
3. Verify proper error handling

**Expected Results**:
- User is redirected to sign-in page
- Appropriate error message is displayed
- Session is cleared

### 4. Error Handling Testing

#### Test Case 4.1: Network Error Handling
**Objective**: Verify network errors are handled gracefully

**Steps**:
1. Temporarily disable network connectivity
2. Attempt an API request
3. Verify error message display
4. Restore network connectivity
5. Verify retry functionality

**Expected Results**:
- Clear error message is displayed
- Retry mechanism is available
- UI remains responsive

#### Test Case 4.2: API Error Handling
**Objective**: Verify API errors are handled gracefully

**Steps**:
1. Cause an API error (e.g., invalid input)
2. Verify error response handling
3. Check user feedback

**Expected Results**:
- Error message is displayed to user
- UI doesn't crash
- Proper error boundaries handle exceptions

### 5. Data Isolation Testing

#### Test Case 5.1: User Data Separation
**Objective**: Verify users only see their own data

**Steps**:
1. Log in as User A
2. Create several tasks
3. Log out
4. Log in as User B
5. Verify User B only sees their own tasks

**Expected Results**:
- Each user only sees their own tasks
- No cross-user data leakage
- Backend enforces data isolation

## Automated Testing Commands

### Run All Tests
```bash
npm run test
# or
yarn test
```

### Run Integration Tests Only
```bash
npm run test:integration
# or
yarn test:integration
```

### Run API Integration Tests
```bash
npm run test:api
# or
yarn test:api
```

## API Endpoint Verification

### Authentication Endpoints
```bash
# Register new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "securePassword123"}'

# Login user
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securePassword123"}'
```

### Task Management Endpoints
```bash
# Get user tasks (requires authentication token)
curl -X GET http://localhost:8000/tasks \
  -H "Authorization: Bearer <valid_token>"

# Create new task (requires authentication token)
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <valid_token>" \
  -d '{"title": "Test Task", "description": "Test Description", "completed": false}'
```

## Performance Testing

### Load Testing
```bash
# Using Artillery or similar tools
artillery run load-test.yaml
```

### API Response Time Verification
- Authentication requests: < 500ms
- Task CRUD operations: < 300ms
- Data retrieval: < 200ms

## Security Testing

### JWT Token Validation
- Verify tokens are properly signed
- Test token expiration handling
- Validate token refresh mechanisms

### Input Validation
- Test for SQL injection
- Test for XSS vulnerabilities
- Validate all user inputs

## Browser Compatibility Testing

Test the application in the following browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Mobile Responsiveness Testing

- Test on various screen sizes
- Verify touch interactions work properly
- Check that forms are usable on mobile

## Final Verification Checklist

- [ ] All authentication flows work correctly
- [ ] Task CRUD operations function properly
- [ ] Protected routes redirect unauthenticated users
- [ ] JWT tokens are properly managed
- [ ] Error handling is graceful
- [ ] Data isolation is maintained
- [ ] API responses are timely
- [ ] UI is responsive and intuitive
- [ ] All tests pass successfully
- [ ] Performance benchmarks are met

## Troubleshooting Common Issues

### Issue 1: API Requests Returning 401
**Cause**: Expired or invalid authentication token
**Solution**: Clear browser storage and re-authenticate

### Issue 2: Tasks Not Appearing
**Cause**: Backend API not returning user's tasks
**Solution**: Verify user ID is being sent correctly with requests

### Issue 3: Slow API Responses
**Cause**: Network latency or backend performance issues
**Solution**: Check backend server health and database performance

## Reporting Test Results

Document all test results in the following format:

```
Test Case: [Name]
Status: [Pass/Fail]
Environment: [Details]
Timestamp: [Date/Time]
Notes: [Any additional information]
```

## Conclusion

Successful completion of all integration tests confirms that the frontend application is properly integrated with the backend API and ready for production deployment.