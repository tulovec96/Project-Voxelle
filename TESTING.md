# Testing Guide for Voxelle

Comprehensive guide for writing, running, and maintaining tests in the Voxelle project.

## Table of Contents

- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Unit Testing](#unit-testing)
- [Integration Testing](#integration-testing)
- [Async Testing](#async-testing)
- [Mocking and Fixtures](#mocking-and-fixtures)
- [Code Coverage](#code-coverage)
- [Best Practices](#best-practices)

---

## Quick Start

### Install Test Dependencies

```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_validators.py -v
```

---

## Test Structure

### Directory Organization

```
tests/
├── __init__.py
├── conftest.py                 # Shared fixtures and configuration
├── test_exceptions.py          # Exception system tests
├── test_validators.py          # Validation function tests
├── test_response_utils.py      # Response formatting tests
├── test_operations/            # Operation layer tests
│   ├── __init__.py
│   ├── test_tts.py            # Text-to-speech tests
│   ├── test_stt.py            # Speech-to-text tests
│   └── test_t2t.py            # Text-to-text tests
├── test_integrations/          # Integration tests
│   ├── __init__.py
│   ├── test_discord.py         # Discord bot tests
│   └── test_twitch.py          # Twitch integration tests
└── test_api/                   # API endpoint tests
    ├── __init__.py
    └── test_endpoints.py       # REST API tests
```

### Naming Conventions

- Test files: `test_<module>.py`
- Test classes: `Test<Component>`
- Test methods: `test_<scenario>`

### Example Structure

```python
# tests/test_module.py
"""Tests for module functionality."""

import pytest
from src.module import function_to_test

class TestFunctionToTest:
    """Test group for function_to_test."""
    
    def test_happy_path(self):
        """Test successful execution."""
        ...
    
    def test_edge_case(self):
        """Test edge case handling."""
        ...
    
    def test_error_handling(self):
        """Test error scenarios."""
        ...
```

---

## Unit Testing

### Basic Unit Test

```python
"""Tests for validators module."""

import pytest
from src.utils.validators import validate_string
from src.utils.exceptions import ValidationError

class TestValidateString:
    """Test string validation."""
    
    def test_valid_string(self):
        """Valid string should pass validation."""
        result = validate_string("valid_string")
        assert result == "valid_string"
    
    def test_empty_string_raises_error(self):
        """Empty string should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_string("")
    
    def test_string_too_long(self):
        """String exceeding max_length should raise error."""
        with pytest.raises(ValidationError):
            validate_string("x" * 100, max_length=50)
    
    def test_min_length_validation(self):
        """String below min_length should raise error."""
        with pytest.raises(ValidationError):
            validate_string("ab", min_length=3)
    
    @pytest.mark.parametrize("input_val,expected", [
        ("hello", "hello"),
        ("world", "world"),
    ])
    def test_multiple_inputs(self, input_val, expected):
        """Test multiple valid inputs."""
        result = validate_string(input_val)
        assert result == expected
```

### Testing Exceptions

```python
"""Tests for exception handling."""

import pytest
from src.utils.exceptions import ValidationError, OperationError

class TestExceptions:
    """Test custom exception classes."""
    
    def test_validation_error_creation(self):
        """ValidationError should store context."""
        error = ValidationError("Invalid input", context={"field": "email"})
        assert error.context["field"] == "email"
    
    def test_exception_message(self):
        """Exception should have readable message."""
        error = ValidationError("Test error")
        assert str(error) == "Test error"
    
    def test_operation_error_component(self):
        """OperationError should track component."""
        error = OperationError("Failed", component="tts")
        assert error.component == "tts"
```

---

## Integration Testing

### Testing API Endpoints

```python
"""Tests for API endpoints."""

import pytest
from src.server.app_server import app

@pytest.fixture
async def client():
    """Create test client."""
    async with app.test_client() as client:
        yield client

class TestAPIEndpoints:
    """Test API endpoint functionality."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Health check endpoint should return 200."""
        response = await client.get("/health")
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_process_text_endpoint(self, client):
        """Text processing endpoint should accept POST."""
        response = await client.post(
            "/api/process",
            json={"text": "Hello world"}
        )
        assert response.status_code == 200
        data = await response.get_json()
        assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_validation_error_returns_400(self, client):
        """Invalid input should return 400."""
        response = await client.post(
            "/api/process",
            json={}  # Missing required 'text' field
        )
        assert response.status_code == 400
```

### Testing with Mocked Dependencies

```python
"""Tests with mocked external dependencies."""

import pytest
from unittest.mock import AsyncMock, patch
from src.operations.tts.manager import TTSManager

class TestTTSWithMocks:
    """Test TTS operation with mocked backend."""
    
    @pytest.mark.asyncio
    async def test_tts_synthesis_mocked(self):
        """Test TTS with mocked audio backend."""
        with patch("src.operations.tts.manager.AudioBackend") as mock_backend:
            mock_backend.synthesize = AsyncMock(
                return_value=b"audio_data"
            )
            
            manager = TTSManager()
            result = await manager.synthesize("Hello world")
            
            assert result == b"audio_data"
            mock_backend.synthesize.assert_called_once()
```

---

## Async Testing

### Testing Async Functions

```python
"""Tests for async operations."""

import pytest
import asyncio

class TestAsyncOperations:
    """Test asynchronous functionality."""
    
    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async function execution."""
        async def async_operation():
            await asyncio.sleep(0.1)
            return "result"
        
        result = await async_operation()
        assert result == "result"
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent operation execution."""
        async def operation(n):
            await asyncio.sleep(0.1)
            return n * 2
        
        results = await asyncio.gather(
            operation(1),
            operation(2),
            operation(3)
        )
        assert results == [2, 4, 6]
    
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test async context manager."""
        class AsyncResource:
            async def __aenter__(self):
                await asyncio.sleep(0.01)
                return self
            
            async def __aexit__(self, *args):
                await asyncio.sleep(0.01)
        
        async with AsyncResource() as resource:
            assert resource is not None
```

### Async Fixtures

```python
"""Async fixtures for testing."""

import pytest
import aiohttp

@pytest.fixture
async def async_client():
    """Create async HTTP client."""
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.fixture
async def mock_async_resource():
    """Create mock async resource."""
    class MockResource:
        async def fetch(self):
            return {"status": "ok"}
    
    return MockResource()
```

---

## Mocking and Fixtures

### Common Fixtures

```python
# tests/conftest.py
"""Shared test configuration and fixtures."""

import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def sample_user_data():
    """Provide sample user data."""
    return {
        "user_id": 123,
        "username": "test_user",
        "email": "test@example.com"
    }

@pytest.fixture
def sample_config():
    """Provide sample configuration."""
    return {
        "api_key": "test-api-key",
        "model": "default",
        "timeout": 30
    }

@pytest.fixture
def mock_database():
    """Provide mock database."""
    mock = MagicMock()
    mock.query = MagicMock(return_value=[{"id": 1}])
    return mock

@pytest.fixture
async def mock_external_api():
    """Provide mock external API."""
    mock = AsyncMock()
    mock.fetch = AsyncMock(return_value={"status": "ok"})
    return mock
```

### Using Fixtures

```python
"""Tests using fixtures."""

class TestUserOperations:
    """Test user operations."""
    
    def test_user_creation(self, sample_user_data):
        """Test user creation with fixture data."""
        user = create_user(sample_user_data)
        assert user.username == "test_user"
    
    def test_database_query(self, mock_database):
        """Test with mocked database."""
        result = mock_database.query()
        assert len(result) == 1
    
    @pytest.mark.asyncio
    async def test_api_call(self, mock_external_api):
        """Test with mocked API."""
        result = await mock_external_api.fetch()
        assert result["status"] == "ok"
```

### Patching

```python
"""Tests with object patching."""

from unittest.mock import patch

class TestWithPatching:
    """Test with patched objects."""
    
    @patch("src.operations.tts.manager.SAMPLE_RATE", 22050)
    def test_with_patched_constant(self):
        """Test with patched constant."""
        from src.operations.tts.manager import SAMPLE_RATE
        assert SAMPLE_RATE == 22050
    
    @patch("src.utils.validators.validate_string")
    def test_with_patched_function(self, mock_validate):
        """Test with patched function."""
        mock_validate.return_value = "mocked_result"
        result = mock_validate("input")
        assert result == "mocked_result"
```

---

## Code Coverage

### Running Coverage Reports

```bash
# Generate coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Coverage with specific modules
pytest --cov=src/utils --cov-report=html

# Show missing lines
pytest --cov=src --cov-report=term-missing
```

### Coverage Configuration

Create `pyproject.toml` section:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/venv/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

### Coverage Goals

- **Critical Paths**: 100% coverage for core business logic
- **Utilities**: >90% coverage for utility functions
- **Integrations**: >80% coverage for external integrations
- **Overall**: >80% project-wide coverage

---

## Best Practices

### ✅ Do's

```python
# ✅ DO: Clear, descriptive test names
def test_validate_email_with_valid_address_returns_true():
    pass

# ✅ DO: Arrange-Act-Assert pattern
def test_calculation():
    # Arrange
    calculator = Calculator()
    
    # Act
    result = calculator.add(2, 3)
    
    # Assert
    assert result == 5

# ✅ DO: Use fixtures for common setup
@pytest.fixture
def app():
    return create_app()

# ✅ DO: Test one thing per test
def test_single_scenario():
    assert function_under_test() == expected_value

# ✅ DO: Handle async properly
@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result is not None
```

### ❌ Don'ts

```python
# ❌ DON'T: Vague test names
def test_function():
    pass

# ❌ DON'T: Test multiple scenarios in one test
def test_everything():
    assert something()
    assert something_else()
    assert another_thing()

# ❌ DON'T: Hardcode dependencies
def test_with_hardcoded_db():
    db = connect_to_real_database()  # Don't do this!
    pass

# ❌ DON'T: Test implementation details
def test_internal_variable():
    obj = MyClass()
    assert obj._private_var == 5  # Don't test private details

# ❌ DON'T: Mix test logic
def test_mixed_concerns():
    user = create_user()  # Setup
    validate_user(user)   # This should be separate
    save_user(user)       # This should be separate
```

### Test Checklist

- [ ] Test runs independently
- [ ] Test is deterministic (same input = same output)
- [ ] Test has descriptive name
- [ ] Test follows AAA pattern
- [ ] Test is fast (<1s)
- [ ] Test cleans up resources
- [ ] Test covers happy path
- [ ] Test covers error cases
- [ ] Test covers edge cases
- [ ] Test uses appropriate assertions

---

## Running Tests in CI/CD

Tests automatically run on:
- Push to `main` or `develop` branches
- Pull requests
- Manual workflow trigger

See `.github/workflows/ci-cd.yml` for CI configuration.

---

For questions about testing, see [CONTRIBUTING.md](CONTRIBUTING.md) or [ADVANCED_DEVELOPMENT.md](ADVANCED_DEVELOPMENT.md).
