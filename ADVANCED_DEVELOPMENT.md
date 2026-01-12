# Advanced Development Guide

This guide covers advanced topics for contributors working on Voxelle's core architecture.

## Table of Contents

- [Project Architecture](#project-architecture)
- [Async/Await Patterns](#asyncawait-patterns)
- [Exception Handling System](#exception-handling-system)
- [Input Validation Framework](#input-validation-framework)
- [Logging Architecture](#logging-architecture)
- [Response Formatting](#response-formatting)
- [Testing Strategy](#testing-strategy)
- [Performance Optimization](#performance-optimization)
- [Debugging Techniques](#debugging-techniques)

---

## Project Architecture

### Core Components

```
Voxelle
├── Core Server (src/)
│   ├── Operations Layer (operations/)
│   │   ├── Text-to-Text (t2t/)
│   │   ├── Speech-to-Text (stt/)
│   │   ├── Text-to-Speech (tts/)
│   │   └── Audio Filtering (filter_audio/)
│   ├── Process Management (processes/)
│   ├── Prompt Engineering (prompter/)
│   ├── Utilities (utils/)
│   └── Server (server/)
│
├── Integrations (apps/)
│   ├── Discord Bot (discord/)
│   ├── Twitch Integration (twitch/)
│   ├── VTube Studio (vts/)
│   └── Web Frontend (frontend/)
│
└── Supporting Structure
    ├── Models (models/)
    ├── Prompts (prompts/)
    ├── Configs (configs/)
    └── Logs (logs/)
```

### Dependency Flow

```
User Request
    ↓
API Endpoint (server/app_server.py)
    ↓
Validators (utils/validators.py)
    ↓
Operation Manager (operations/manager.py)
    ↓
Specific Operation (operations/*/manager.py)
    ↓
Response Formatter (utils/response_utils.py)
    ↓
User Response
```

---

## Async/Await Patterns

### Basic Async Function

All I/O operations should be async to prevent blocking:

```python
async def fetch_model_config(model_name: str) -> dict:
    """Fetch model configuration asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/models/{model_name}") as resp:
            return await resp.json()
```

### Async Context Managers

Use context managers to ensure resource cleanup:

```python
async def process_audio_stream(stream_url: str) -> bytes:
    """Process audio from stream with automatic cleanup."""
    async with aiohttp.ClientSession() as session:
        async with session.get(stream_url) as response:
            audio_data = await response.read()
    # Session automatically closed here
    return audio_data
```

### Concurrent Operations

Use `asyncio.gather()` for parallel operations:

```python
async def process_multiple_requests(requests: list[dict]) -> list[dict]:
    """Process multiple requests concurrently."""
    tasks = [process_single_request(req) for req in requests]
    results = await asyncio.gather(*tasks)
    return results
```

### Task Timeouts

Always set timeouts on async operations:

```python
async def fetch_with_timeout(url: str, timeout: int = 30) -> dict:
    """Fetch data with timeout protection."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                return await resp.json()
    except asyncio.TimeoutError:
        raise OperationError(f"Request to {url} timed out after {timeout}s")
```

---

## Exception Handling System

### Exception Hierarchy

```
VoxelleException (base)
├── ValidationError
├── ConfigurationError
├── OperationError
│   ├── TTSError
│   ├── STTError
│   ├── T2TError
│   └── AudioFilterError
├── ProcessError
├── APIError
│   ├── AuthenticationError
│   ├── AuthorizationError
│   └── RateLimitError
└── BackendError
    ├── DatabaseError
    └── IntegrationError
```

### Using Custom Exceptions

```python
from src.utils.exceptions import ValidationError, OperationError

def validate_and_process(data: dict) -> dict:
    """Validate input and process with proper error handling."""
    try:
        # Validate input
        if not data.get("text"):
            raise ValidationError("text field is required")
        
        # Process data
        result = process_text(data["text"])
        return result
        
    except ValidationError as e:
        # Handle validation errors (user error)
        logger.warning(f"Validation failed: {e.context}")
        return create_error_response(str(e), 400)
        
    except OperationError as e:
        # Handle operation errors (system error)
        logger.error(f"Operation failed: {e.context}")
        return create_error_response("Processing failed", 500)
```

### Exception Context

All custom exceptions include context information:

```python
try:
    perform_operation()
except OperationError as e:
    print(e.context)  # Structured error context
    print(e.timestamp)  # When error occurred
    print(e.component)  # Which component failed
```

---

## Input Validation Framework

### Validation Chain

```python
from src.utils.validators import validate_string, validate_integer, validate_list

def process_user_request(data: dict) -> dict:
    """Process request with comprehensive validation."""
    try:
        # Validate individual fields
        username = validate_string(
            data.get("username"),
            min_length=3,
            max_length=32,
            pattern=r"^[a-zA-Z0-9_]+$"
        )
        
        age = validate_integer(
            data.get("age"),
            min_value=0,
            max_value=150
        )
        
        tags = validate_list(
            data.get("tags"),
            element_type=str,
            max_length=10
        )
        
        # All validations passed
        return {
            "username": username,
            "age": age,
            "tags": tags
        }
        
    except ValidationError as e:
        return {"error": str(e)}
```

### Custom Validators

Extend validation for domain-specific needs:

```python
from src.utils.validators import validate_string

def validate_discord_token(token: str) -> str:
    """Validate Discord bot token format."""
    token = validate_string(token, min_length=50, max_length=100)
    
    if not token.startswith("MTA") and not token.startswith("MzI"):
        raise ValidationError("Invalid Discord token format")
    
    return token
```

---

## Logging Architecture

### Log Categories

```python
from src.utils.logging_utils import LogCategory

# Available categories:
LogCategory.OPERATION      # Core business operations
LogCategory.INTEGRATION    # Discord, Twitch, VTS interactions
LogCategory.SECURITY       # Authentication, authorization, suspicious activity
LogCategory.PERFORMANCE    # Timing, resource usage
LogCategory.API_REQUEST    # HTTP requests and responses
LogCategory.ERROR          # Errors and exceptions
```

### Logging Usage

```python
from src.utils.logging_utils import (
    log_operation_start,
    log_operation_complete,
    log_security_event,
    log_performance
)
import logging

logger = logging.getLogger(__name__)

# Log operation lifecycle
log_operation_start("text_processing", {"user_id": 123, "text_length": 256})

try:
    result = process_text(text)
    log_operation_complete("text_processing", {"output_length": len(result)})
except Exception as e:
    logger.error(f"Text processing failed: {e}", exc_info=True)

# Log security events
log_security_event(
    "failed_authentication",
    {"user_id": 123, "attempt_count": 5, "action": "block"}
)

# Log performance metrics
log_performance("database_query", 0.125)  # 125ms
```

---

## Response Formatting

### Standard Response Structure

All API responses follow a consistent format:

```python
from src.utils.response_utils import (
    create_success_response,
    create_error_response,
    create_paginated_response
)

# Success response
response = create_success_response(
    "Operation completed successfully",
    {
        "result": process_result,
        "duration_ms": 250
    }
)

# Error response
error_response = create_error_response(
    "Invalid input parameters",
    400  # HTTP status code
)

# Paginated response
paginated = create_paginated_response(
    items=query_results,
    total=1000,
    page=1,
    per_page=20
)
```

### Response Format Example

```json
{
  "success": true,
  "message": "Operation completed",
  "data": {
    "result": "processed_data"
  },
  "timestamp": "2024-01-15T10:30:45.123Z",
  "request_id": "req-123456"
}
```

---

## Testing Strategy

### Test Structure

```
tests/
├── test_exceptions.py      # Exception system
├── test_validators.py      # Validation functions
├── test_response_utils.py  # Response formatting
├── test_operations/        # Operation layer
│   ├── test_tts.py
│   ├── test_stt.py
│   └── test_t2t.py
├── test_integrations/      # Discord, Twitch, VTS
└── test_api/               # API endpoints
```

### Test Patterns

```python
import pytest
from src.utils.validators import validate_email
from src.utils.exceptions import ValidationError

class TestEmailValidation:
    """Test email validation function."""
    
    def test_valid_email(self):
        """Valid email should return True."""
        assert validate_email("user@example.com") is True
    
    def test_invalid_email_format(self):
        """Invalid format should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_email("not-an-email")
    
    def test_empty_email_raises_error(self):
        """Empty email should raise ValueError."""
        with pytest.raises(ValueError):
            validate_email("")
    
    @pytest.mark.asyncio
    async def test_async_operation(self):
        """Test async operations."""
        result = await fetch_async_data()
        assert result is not None
    
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("test+tag@domain.co.uk", True),
        ("invalid@", False),
    ])
    def test_multiple_emails(self, email, expected):
        """Test multiple email formats."""
        assert validate_email(email) == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_validators.py -v

# Run with detailed output
pytest -vv --tb=short

# Run only fast tests (skip slow ones)
pytest -m "not slow"
```

---

## Performance Optimization

### Async Pattern Optimization

```python
# ❌ SLOW: Sequential operations
async def slow_process():
    result1 = await operation1()
    result2 = await operation2()
    result3 = await operation3()

# ✅ FAST: Parallel operations
async def fast_process():
    results = await asyncio.gather(
        operation1(),
        operation2(),
        operation3()
    )
    result1, result2, result3 = results
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user_preferences(user_id: int) -> dict:
    """Cache expensive user preference lookups."""
    return fetch_preferences_from_db(user_id)

# Clear cache when preferences change
get_user_preferences.cache_clear()

# Get cache info
print(get_user_preferences.cache_info())
```

### Connection Pooling

```python
import aiohttp

# Create session with connector pooling
connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
session = aiohttp.ClientSession(connector=connector)

# Use session across multiple requests
await session.get("https://api1.com/data")
await session.get("https://api2.com/data")

# Close when done
await session.close()
```

---

## Debugging Techniques

### Debug Logging

```python
import logging

# Set debug level
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_function(value: int) -> int:
    """Function with debug logging."""
    logger.debug(f"Input value: {value}")
    result = value * 2
    logger.debug(f"Computed result: {result}")
    return result
```

### Breakpoint Debugging

```python
def complex_operation(data: dict) -> dict:
    """Complex operation with debugging."""
    
    # Pause execution here for inspection
    breakpoint()  # Python 3.7+
    
    # Or use pdb:
    # import pdb; pdb.set_trace()
    
    result = process(data)
    return result
```

### Performance Profiling

```python
import timeit
from functools import wraps
import time

def timer_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {(end - start)*1000:.2f}ms")
        return result
    return wrapper

@timer_decorator
def slow_operation():
    """Measure execution time."""
    time.sleep(1)
```

---

## Contributing to Core Components

### Adding a New Operation

1. Create new directory in `src/operations/<operation_name>/`
2. Implement manager class inheriting from `OperationManager`
3. Add input validation using validators
4. Use custom exceptions for error handling
5. Return responses using response utilities
6. Write comprehensive tests

### Extending Validators

1. Add new validation function to `src/utils/validators.py`
2. Use appropriate exception types
3. Write tests covering valid and invalid inputs
4. Document in docstring with examples

### Adding New Integration

1. Create new directory in `apps/<integration_name>/`
2. Implement connection and event handlers
3. Use logging utilities for tracking
4. Handle disconnections gracefully
5. Write integration tests

---

For questions about advanced development, please open an issue or contact the core team.
