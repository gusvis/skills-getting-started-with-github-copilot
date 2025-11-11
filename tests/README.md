# Tests for Mergington High School API

This directory contains comprehensive tests for the Mergington High School extracurricular activities API.

## 🧪 Implemented Tests

### Covered Functionalities
- ✅ **Get activities**: Test for GET `/activities` endpoint
- ✅ **Activity signup**: Test for POST `/activities/{activity_name}/signup` endpoint
- ✅ **Cancel registrations**: Test for DELETE `/activities/{activity_name}/cancel` endpoint
- ✅ **View participants**: Test for GET `/activities/{activity_name}/participants` endpoint
- ✅ **Business validations**: Maximum capacity, valid emails, duplicates

### Test Cases
1. **test_root_redirect**: Verifies root redirection
2. **test_get_activities**: Gets all activities
3. **test_signup_for_activity_success**: Successful signup
4. **test_signup_for_nonexistent_activity**: Error for non-existent activity
5. **test_signup_duplicate_student**: Prevent duplicate registrations
6. **test_signup_activity_full**: Maximum capacity handling
7. **test_signup_invalid_email_domain**: Email domain validation
8. **test_cancel_activity_signup_success**: Successful cancellation
9. **test_cancel_nonexistent_activity**: Error when canceling non-existent activity
10. **test_cancel_student_not_signed_up**: Error when canceling unregistered student
11. **test_get_activity_participants_success**: Get participant list
12. **test_get_participants_nonexistent_activity**: Error for non-existent activity
13. **test_get_participants_empty_activity**: Activity with no participants
14. **test_activity_capacity_management**: Complete capacity management

## 🚀 How to Run the Tests

### Option 1: Automated script
```bash
./run_tests.sh
```

### Option 2: Direct command
```bash
# Basic tests
python -m pytest tests/ -v

# Tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Tests with HTML report
python -m pytest tests/ --cov=src --cov-report=html
```

## 📊 Code Coverage

- **Current coverage**: 100% 🎉
- **Lines covered**: 43/43
- **HTML report**: `htmlcov/index.html`

## 🛠️ Dependencies

The following dependencies are required to run the tests:

```
pytest
pytest-asyncio
pytest-cov
httpx
```

## 🏗️ Test Structure

```
tests/
├── __init__.py          # Package initialization
├── conftest.py          # Configuration and shared fixtures
├── test_api.py          # Main API tests
└── README.md           # This documentation
```

## 🔧 Available Fixtures

- **client**: FastAPI test client
- **reset_activities**: Resets activity data before each test

## 📝 Notes

- Tests use in-memory data that resets between each test
- Each test is independent and doesn't affect others
- Both success and error cases are validated
- Code coverage is 100%