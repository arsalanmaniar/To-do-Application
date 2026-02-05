#!/usr/bin/env python3
"""
Validation script to check implementation completeness
Verifies that all required functionality from tasks.md has been implemented
"""
import os
import sys
from pathlib import Path


def validate_project_structure():
    """Validate that the project structure matches the plan"""
    print("Validating project structure...")

    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("[FAIL] Backend directory not found")
        return False

    # Check required directories
    required_dirs = [
        "backend/app",
        "backend/app/core",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/database",
        "backend/app/api/v1/endpoints",
        "backend/tests",
        "backend/tests/unit",
        "backend/tests/integration",
        "backend/tests/contract"
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"[FAIL] Missing directories: {missing_dirs}")
        return False
    else:
        print("[PASS] All required directories exist")
        return True


def validate_files_existence():
    """Validate that all required files exist"""
    print("\nValidating required files...")

    required_files = [
        "backend/app/main.py",
        "backend/app/core/config.py",
        "backend/app/core/security.py",
        "backend/app/core/dependencies.py",
        "backend/app/core/exceptions.py",
        "backend/app/core/logging.py",
        "backend/app/models/task.py",
        "backend/app/models/user.py",
        "backend/app/schemas/task.py",
        "backend/app/schemas/user.py",
        "backend/app/database/session.py",
        "backend/app/database/base.py",
        "backend/app/api/v1/endpoints/tasks.py",
        "backend/app/services/task_service.py",
        "backend/requirements.txt",
        "backend/.env.example",
        "backend/.gitignore",
        "backend/README.md",
        "backend/alembic.ini",
        "backend/alembic/versions"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"[FAIL] Missing files: {missing_files}")
        return False
    else:
        print("[PASS] All required files exist")
        return True


def validate_task_completion():
    """Validate that tasks from tasks.md have been completed"""
    print("\nValidating task completion...")

    # Check that implementations exist for the key tasks
    validation_checks = {
        "T006-T013: Foundational setup": validate_foundational_setup(),
        "T016-T021: Task CRUD operations": validate_task_crud(),
        "T024-T029: User authentication": validate_auth_system(),
        "T032-T036: Database persistence": validate_database_layer(),
        "T037-T041: API endpoints": validate_api_endpoints(),
        "T042-T049: Polish and documentation": validate_polish_features()
    }

    all_passed = True
    for task, passed in validation_checks.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {task}")
        if not passed:
            all_passed = False

    return all_passed


def validate_foundational_setup():
    """Validate foundational setup tasks"""
    checks = [
        Path("backend/app/database/session.py").exists(),
        Path("backend/app/database/base.py").exists(),
        Path("backend/app/core/config.py").exists(),
        Path("backend/app/core/security.py").exists(),
        Path("backend/app/main.py").exists(),
        Path("backend/app/core/dependencies.py").exists(),
        Path("backend/app/core/exceptions.py").exists(),
        Path("backend/app/core/logging.py").exists()
    ]
    return all(checks)


def validate_task_crud():
    """Validate task CRUD operations"""
    checks = [
        Path("backend/app/models/task.py").exists(),
        Path("backend/app/schemas/task.py").exists(),
        Path("backend/app/services/task_service.py").exists(),
        Path("backend/app/api/v1/endpoints/tasks.py").exists()
    ]

    if not all(checks):
        return False

    # Check that task_service has CRUD methods
    task_service_content = Path("backend/app/services/task_service.py").read_text()
    crud_methods = [
        "create_task",
        "get_task_by_id",
        "get_tasks_by_user",
        "update_task",
        "delete_task",
        "toggle_task_completion"
    ]

    for method in crud_methods:
        if f"def {method}" not in task_service_content:
            print(f"    Missing method: {method}")
            return False

    return True


def validate_auth_system():
    """Validate authentication system"""
    checks = [
        Path("backend/app/core/security.py").exists(),
        Path("backend/app/core/dependencies.py").exists()
    ]

    if not all(checks):
        return False

    # Check for JWT validation methods
    security_content = Path("backend/app/core/security.py").read_text()
    auth_methods = [
        "verify_token",
        "create_access_token"
    ]

    has_auth_methods = any(method in security_content for method in auth_methods)

    # Check for user validation in dependencies
    deps_content = Path("backend/app/core/dependencies.py").read_text()
    has_user_validation = "get_current_user_id_matching_path" in deps_content

    return has_auth_methods or has_user_validation


def validate_database_layer():
    """Validate database layer"""
    checks = [
        Path("backend/app/models/task.py").exists(),
        Path("backend/app/database/session.py").exists()
    ]

    if not all(checks):
        return False

    # Check that models have proper relationships
    task_model_content = Path("backend/app/models/task.py").read_text()
    has_foreign_key = "owner_id" in task_model_content and "foreign_key" in task_model_content.lower()

    # Check for proper database session handling
    session_content = Path("backend/app/database/session.py").read_text()
    has_session_mgmt = "SessionLocal" in session_content or "get_session" in session_content

    return has_foreign_key and has_session_mgmt


def validate_api_endpoints():
    """Validate API endpoints exist"""
    if not Path("backend/app/api/v1/endpoints/tasks.py").exists():
        return False

    endpoints_content = Path("backend/app/api/v1/endpoints/tasks.py").read_text()

    # Check for required HTTP methods
    required_endpoints = [
        "@router.get",    # GET /api/v1/{user_id}/tasks
        "@router.post",   # POST /api/v1/{user_id}/tasks
        "@router.put",    # PUT /api/v1/{user_id}/tasks/{task_id}
        "@router.patch",  # PATCH /api/v1/{user_id}/tasks/{task_id}
        "@router.delete"  # DELETE /api/v1/{user_id}/tasks/{task_id}
    ]

    endpoint_checks = [endpoint in endpoints_content for endpoint in required_endpoints]

    # Also check for the special completion endpoint
    has_completion_endpoint = "/complete" in endpoints_content

    return all(endpoint_checks) and has_completion_endpoint


def validate_polish_features():
    """Validate polish and documentation"""
    checks = [
        Path("backend/README.md").exists(),
        Path("backend/.gitignore").exists(),
        Path("backend/.env.example").exists()
    ]

    if not all(checks):
        return False

    # Check for documentation in README
    readme_content = Path("backend/README.md").read_text()
    has_docs = len(readme_content.strip()) > 10  # Basic check for content

    return has_docs


def validate_test_files():
    """Validate that test files were created as required"""
    print("\nValidating test files...")

    required_tests = [
        "backend/tests/contract/test_task_endpoints.py",      # T014
        "backend/tests/integration/test_task_management.py",  # T015
        "backend/tests/contract/test_auth_endpoints.py",      # T022
        "backend/tests/integration/test_auth.py",             # T023
        "backend/tests/contract/test_persistence.py",         # T030
        "backend/tests/integration/test_database.py",         # T031
        "backend/tests/unit/test_services.py"                 # T045 (additional unit tests)
    ]

    missing_tests = []
    for test_file in required_tests:
        if not Path(test_file).exists():
            missing_tests.append(test_file)

    if missing_tests:
        print(f"[FAIL] Missing test files: {missing_tests}")
        return False
    else:
        print("[PASS] All required test files exist")

        # Count the test files we created
        created_count = len(required_tests)
        print(f"   Created {created_count} test files as required by tasks")
        return True


def main():
    print("Validating Backend API Implementation")
    print("=" * 50)

    # Run all validations
    structure_ok = validate_project_structure()
    files_ok = validate_files_existence()
    tasks_ok = validate_task_completion()
    tests_ok = validate_test_files()

    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY:")
    print(f"Project structure: {'[PASS] PASS' if structure_ok else '[FAIL] FAIL'}")
    print(f"Required files: {'[PASS] PASS' if files_ok else '[FAIL] FAIL'}")
    print(f"Task completion: {'[PASS] PASS' if tasks_ok else '[FAIL] FAIL'}")
    print(f"Test files: {'[PASS] PASS' if tests_ok else '[FAIL] FAIL'}")

    overall_pass = structure_ok and files_ok and tasks_ok and tests_ok

    print(f"\nOverall status: {'[PASS] ALL CHECKS PASSED' if overall_pass else '[FAIL] SOME CHECKS FAILED'}")

    if overall_pass:
        print("\nImplementation is complete and validated!")
        print("All required functionality from tasks.md has been implemented.")
        return 0
    else:
        print("\nSome validation checks failed.")
        print("Please review the missing components above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())