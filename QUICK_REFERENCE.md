# Quick Reference for Voxelle Developers

## Setup (5 minutes)

```bash
# 1. Clone and enter directory
git clone https://github.com/tulovec96/Project-Voxelle.git
cd Project-Voxelle

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 3. Install development dependencies
pip install -e ".[dev]"
pre-commit install

# 4. Run tests to verify setup
pytest
```

---

## Common Commands

### Development

```bash
# Run development server
python src/main.py

# Run with debug logging
make debug

# Run tests
pytest              # all tests
pytest -v           # verbose
pytest --cov        # with coverage

# Code formatting
make format         # auto-fix formatting
make lint          # check linting
make type-check    # check types
make security      # security scan

# All checks
make all-checks    # format + lint + types + security + tests
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, then...

# Stage changes
git add src/

# Commit with conventional format
git commit -m "feat(module): add new feature"

# Push
git push origin feature/my-feature

# Create PR on GitHub
```

---

## Code Examples

### Exception Handling

```python
from src.utils.exceptions import ValidationError

try:
    # Your code
    pass
except ValidationError as e:
    logger.error(f"Validation failed: {e.context}")
```

### Input Validation

```python
from src.utils.validators import validate_string, validate_integer

try:
    username = validate_string(data, min_length=3, max_length=32)
    age = validate_integer(age_data, min_value=0, max_value=150)
except ValidationError as e:
    return create_error_response(str(e), 400)
```

### Logging

```python
from src.utils.logging_utils import log_operation_start, log_operation_complete

log_operation_start("operation_name", {"key": "value"})
try:
    # Your operation
    result = perform_operation()
    log_operation_complete("operation_name", {"result": "success"})
except Exception as e:
    logger.error(f"Failed: {e}")
```

### API Responses

```python
from src.utils.response_utils import create_success_response, create_error_response

# Success
return create_success_response("Operation successful", {"data": result})

# Error
return create_error_response("Invalid input", 400)

# Paginated
return create_paginated_response(items=results, total=100, page=1, per_page=20)
```

### Async Functions

```python
async def fetch_data(url: str) -> dict:
    """Fetch data asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            return await resp.json()
```

### Type Hints

```python
def process_data(text: str, count: int) -> dict[str, Any]:
    """Process text data with count parameter."""
    return {"processed": text, "count": count}
```

### Docstrings

```python
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numeric values.
    
    Returns:
        The arithmetic mean of the numbers.
    
    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
```

---

## File Locations

### Source Code
- Core server: `src/`
- Operations: `src/operations/`
- Process management: `src/processes/`
- Prompt system: `src/prompter/`
- Utilities: `src/utils/`

### Integrations
- Discord: `apps/discord/src/`
- Twitch: `apps/twitch/src/`
- VTube Studio: `apps/vts/src/`
- Frontend: `apps/frontend/src/`

### Configuration & Data
- Configs: `configs/`
- Prompts: `prompts/`
- Models: `models/`
- Logs: `logs/`

### Testing
- Unit tests: `tests/`
- Test config: `tests/conftest.py`

---

## Important Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project configuration, dependencies |
| `requirements.txt` | Production dependencies |
| `requirements-dev.txt` | Development dependencies |
| `src/main.py` | Server entry point |
| `src/utils/exceptions.py` | Exception definitions |
| `src/utils/validators.py` | Input validators |
| `src/utils/logging_utils.py` | Logging utilities |
| `src/utils/response_utils.py` | Response formatting |
| `CONTRIBUTING.md` | Contribution guidelines |
| `ADVANCED_DEVELOPMENT.md` | Architecture & patterns |
| `TESTING.md` | Testing guide |
| `ROADMAP.md` | Development roadmap |

---

## Code Style Rules

### Python
- **Line length**: Max 100 characters
- **Type hints**: Required for all functions
- **Docstrings**: Google style required
- **Naming**: snake_case for functions/variables, PascalCase for classes

### Formatting Tools
- **Black**: Code formatting (automatically applied)
- **isort**: Import sorting (automatically applied)
- **flake8**: Linting (pre-commit check)
- **mypy**: Type checking (pre-commit check)

### Pre-commit Checks
These run automatically before each commit:
- Code formatting (Black, isort)
- Linting (flake8)
- Type checking (mypy)
- Security scanning (Bandit)
- General file checks

---

## Testing Checklist

Before submitting a PR:

- [ ] All tests pass: `pytest`
- [ ] Coverage maintained: `pytest --cov=src`
- [ ] Code formatted: `make format`
- [ ] Linting passes: `make lint`
- [ ] Type checking passes: `make type-check`
- [ ] Security scan passes: `make security`
- [ ] New code has tests
- [ ] New code has docstrings
- [ ] New code has type hints
- [ ] No hardcoded secrets
- [ ] No debug print statements

---

## Useful Resources

### Documentation
- [Contributing Guide](CONTRIBUTING.md)
- [Advanced Development](ADVANCED_DEVELOPMENT.md)
- [Testing Guide](TESTING.md)
- [Docker Guide](DOCKER_GUIDE.md)
- [Roadmap](ROADMAP.md)

### Tools & Libraries
- [Pytest](https://docs.pytest.org/) - Testing framework
- [Black](https://black.readthedocs.io/) - Code formatter
- [mypy](http://mypy-lang.org/) - Type checker
- [Quart](https://quart.palletsprojects.com/) - Async web framework
- [discord.py](https://discordpy.readthedocs.io/) - Discord bot library

### Community
- GitHub Issues: Report bugs and request features
- GitHub Discussions: Ask questions and discuss ideas
- Discord: Real-time community chat (link in README)

---

## Troubleshooting

### Tests Fail After Setup
```bash
# Verify virtual environment is activated
# Run: pip install -e ".[dev]"
# Run: pytest
```

### Code Style Issues
```bash
# Auto-fix formatting
make format

# Check remaining issues
make lint
```

### Type Errors
```bash
# Run type checker
make type-check

# Fix type hints in your code
```

### Permission Errors
```bash
# On Unix: Make scripts executable
chmod +x script.sh

# On Windows: Run terminal as Administrator
```

### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall packages: pip install -e ".[dev]"
```

---

## Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] No debug code

## Closes
Fixes #(issue number)
```

---

## Emergency Contacts

- **Maintainer**: @tulovec96
- **Issues**: GitHub Issues
- **Urgent**: Check README.md for contact info

---

## Key Commands Summary

```bash
# Setup
pip install -e ".[dev]" && pre-commit install

# Development
python src/main.py              # Run server
pytest                          # Run tests
make all-checks                 # Check everything

# Git
git checkout -b feature/name    # New branch
git add .                       # Stage changes
git commit -m "type(scope): msg" # Commit
git push origin feature/name    # Push

# Cleanup
make clean                      # Remove artifacts
rm -rf venv                     # Remove venv
```

---

**Last Updated**: February 2024
**Questions?** See [CONTRIBUTING.md](CONTRIBUTING.md) or open a GitHub issue.
