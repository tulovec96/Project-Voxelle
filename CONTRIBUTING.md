# 🤝 Contributing to Voxelle

<p align="center">
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge" alt="Contributions Welcome">
  <img src="https://img.shields.io/badge/PRs-Welcome-blue?style=for-the-badge" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

Thank you for your interest in contributing to **Voxelle**! This project thrives on community contributions, whether it's code, documentation, bug reports, or feature ideas.

> **Note:** Voxelle is based on [J.A.I.son](https://github.com/limitcantcode/jaison-core) by [@limitcantcode](https://github.com/limitcantcode) **(No Voxelle Support)**. Voxelle is maintained & enhanced by [@tulovec96](https://github.com/tulovec96).

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How to Contribute](#-how-to-contribute)
- [Development Setup](#-development-setup)
- [Code Guidelines](#-code-guidelines)
- [Testing Requirements](#-testing-requirements)
- [Commit Guidelines](#-commit-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Reporting Issues](#-reporting-issues)
- [Questions & Support](#-questions--support)

---

## 📜 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors:

- ✅ Be respectful and considerate
- ✅ Welcome different opinions and experiences
- ✅ Provide constructive feedback
- ✅ Help newcomers learn
- ❌ No harassment, discrimination, or hate speech
- ❌ No spam or self-promotion

---

## 💡 How to Contribute

### 🐛 Found a Bug?

1. **Check existing issues** first
2. **Create a detailed bug report** including:
   - What you were trying to do
   - What you expected vs what happened
   - Your environment (OS, Python 3.14.2, Node.js version)
   - Error messages or logs
   - Steps to reproduce

### 🎯 Have a Feature Idea?

1. **Discuss first** - Open an issue to discuss your idea
2. **Explain the use case** - Why is this feature needed?
3. **Propose an implementation** - How would you build it?

### 📚 Improve Documentation?

Documentation improvements are always welcome! You can:
- Fix typos in README or docs
- Add examples or tutorials
- Clarify confusing sections
- Update outdated information

No approval needed—just submit a PR!

### 🔧 Submit Code

Follow the guidelines below for the best chance of acceptance.

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### 1. Fork & Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/voxelle.git
cd voxelle
```

### 2. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/macOS
```

### 3. Install Development Dependencies

```bash
# Install with development tools
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Frontend dependencies
cd apps/frontend
npm install
cd ../..
```

### 4. Verify Setup

```bash
# Run tests
pytest --version

# Check code style
black --version
isort --version
flake8 --version
mypy --version
```

---

## 📋 Code Guidelines

### Type Hints
Always use type hints for function parameters and return types:

```python
def process_message(text: str, user_id: int) -> dict[str, Any]:
    """Process incoming message and return response data."""
    ...
```

### Docstrings
Use Google-style docstrings with detailed information:

```python
def calculate_sentiment(text: str, model: str = "default") -> float:
    """Calculate sentiment score for given text.

    Args:
        text: The text to analyze for sentiment.
        model: The sentiment model to use. Defaults to "default".

    Returns:
        A float between -1.0 (negative) and 1.0 (positive).

    Raises:
        ValueError: If text is empty or model is invalid.
    """
    ...
```

### Exception Handling
Use custom exceptions from `src/utils/exceptions.py`:

```python
from src.utils.exceptions import ValidationError, OperationError

try:
    validate_user_input(data)
except ValidationError as e:
    logger.error(f"Validation failed: {e.context}")
```

### Logging
Use logging utilities from `src/utils/logging_utils.py`:

```python
from src.utils.logging_utils import log_operation_start, log_operation_complete

log_operation_start("user_registration", {"user_id": user_id})
try:
    register_user(user_id)
    log_operation_complete("user_registration", {"user_id": user_id})
except Exception as e:
    logger.error(f"Failed: {e}")
```

### Code Style

Python code must pass:
- **Black** (code formatting)
- **isort** (import sorting)
- **flake8** (linting)
- **mypy** (type checking)

Pre-commit hooks automatically check these before each commit.

---

## 🧪 Testing Requirements

### Writing Tests
Tests must be placed in `tests/` directory:

```python
import pytest
from src.utils.validators import validate_email

class TestEmailValidation:
    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_invalid_email(self):
        assert validate_email("invalid") is False

    def test_empty_raises_error(self):
        with pytest.raises(ValueError):
            validate_email("")
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_validators.py -v
```

### Coverage Requirements
- Minimum 80% code coverage for new code
- All public APIs must have tests
- Edge cases and error conditions should be tested

---

## 📁 Project Structure

```
voxelle/
├── src/                    # Core AI server
├── apps/
│   ├── discord/            # Discord bot integration
│   ├── twitch/             # Twitch chat integration
│   ├── vts/                # VTube Studio integration
│   └── frontend/           # SvelteKit web dashboard
├── configs/                # Configuration templates
├── prompts/                # AI prompt templates
├── models/                 # AI models directory
├── scripts/                # Utility scripts
├── manager.py              # Project manager CLI
└── requirements.txt        # Python dependencies
```

### Key Files

| File | Purpose |
|------|---------|
| `manager.py` | Main CLI for running services and managing deps |
| `src/main.py` | Core server entry point |
| `apps/*/src/main.py` | App entry points |
| `config.yaml` | Main configuration |

---

## � Security Guidelines

### Protecting Secrets
Never commit sensitive information:
- API keys, tokens, passwords
- Private URLs or IPs
- Database credentials
- OAuth secrets

**Solution:** Use environment variables with `.env` files:

```python
import os
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
database_url = os.getenv("DATABASE_URL")
```

### Input Validation
Always validate user input using validators from `src/utils/validators.py`:

```python
from src.utils.validators import validate_string, validate_integer
from src.utils.exceptions import ValidationError

try:
    username = validate_string(user_input, min_length=3, max_length=32)
    age = validate_integer(age_input, min_value=0, max_value=150)
except ValidationError as e:
    return create_error_response(str(e), 400)
```

### Dependency Security
Keep dependencies up to date and check for vulnerabilities:

```bash
# Update dependencies
pip install --upgrade -e ".[dev]"

# Check for known vulnerabilities
safety check

# Show outdated packages
pip list --outdated
```

### Bandit Security Scanning
Pre-commit hooks run Bandit security checks automatically:

```bash
# Manual security scan
bandit -r src --exclude tests/
```

---

## 📝 Commit Guidelines

### Commit Message Format

Use conventional commits format:

```
type(scope): short description (50 chars or less)

Longer description explaining the change and why it was made.

Fixes #123  # If closing an issue
```

### Commit Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `docs` | Documentation changes |
| `test` | Test additions/changes |
| `chore` | Build, deps, config |
| `ci` | CI/CD pipeline changes |
| `security` | Security-related fixes |

### Examples

```
feat(discord): add custom command framework

fix(validators): handle null values in email validation

docs(DEVELOPER): add API endpoint documentation

test(response_utils): add pagination tests

security(exceptions): sanitize error messages in responses

perf(operations): optimize async request batching
```

---

## 🔄 Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
```

Use meaningful branch names:
- `feature/user-authentication`
- `fix/discord-reconnection-bug`
- `docs/update-setup-guide`
- `perf/async-optimization`

### 2. Make Your Changes

- ✅ Write clear, well-commented code
- ✅ Follow PEP 8 and type hint guidelines
- ✅ Add comprehensive docstrings
- ✅ Update documentation if needed
- ✅ Write/update tests for new functionality
- ✅ Don't commit secrets or debug code

### 3. Pre-commit Verification

Pre-commit hooks run automatically, but you can verify manually:

```bash
# Run all pre-commit checks
pre-commit run --all-files

# Or individually:
black src tests
isort src tests
flake8 src tests
mypy src
pytest
```

### 4. Push & Create Pull Request

```bash
git push origin feature/amazing-feature
```

**Create PR with:**
- Clear title following conventional commits
- Detailed description of changes and motivation
- Link to related issues (use "Fixes #123")
- Screenshots for UI changes
- Test results showing coverage

### 5. PR Review

- Respond to reviewer feedback promptly
- Request changes when needed
- Ensure CI/CD passes completely
- Code coverage should not decrease

### 6. Merge

Once approved:
- Squash and merge for cleaner history (unless multiple logical commits)
- Delete the feature branch
- Close related issues if not auto-closed

---

## 🐛 Reporting Issues

Use the appropriate issue template:

### Bug Report Title Format
```
[BUG] Short description of the bug
```

**Include:**
- OS (Windows/macOS/Linux)
- Python version
- Node.js version (for frontend issues)
- Steps to reproduce (numbered list)
- Expected behavior
- Actual behavior
- Error messages and full stack traces
- Logs from `logs/` directory if available

### Example Bug Report
```
[BUG] Discord bot crashes when sending audio files

**Environment:**
- OS: Windows 11
- Python: 3.11.3
- Bot version: 1.2.0

**Steps to reproduce:**
1. Create voice channel
2. Start bot with `python manager.py start`
3. Send audio file in chat
4. Bot crashes

**Expected:** Audio processes normally
**Actual:** Bot exits with error

**Error log:**
[Full traceback here]
```

---

## 🎯 Feature Requests

**Title Format:**
```
[FEATURE] Short description
```

**Include:**
- Use case (why is this needed?)
- Proposed solution
- Which component (Core, Discord, Twitch, VTS, Frontend)

---

## 💬 Questions & Support

- **Discord**: [Join Community](https://discord.gg/Z8yyEzHsYM)
- **Issues**: Open a GitHub issue with `[QUESTION]` prefix

---

## 🎨 Code Style

### Python
- Follow PEP 8
- Use type hints
- Docstrings for functions

```python
def process_message(text: str, user_id: int) -> dict:
    """Process incoming message and return response data."""
    ...
```

### TypeScript/Svelte
- Use TypeScript for type safety
- Follow existing component patterns
- Use Tailwind utility classes

```svelte
<script lang="ts">
  export let title: string;
  export let active: boolean = false;
</script>
```

---

## 🚀 Review Process

PRs are reviewed as soon as possible. We check:

- ✅ Code quality and style
- ✅ Logic and implementation
- ✅ Documentation updates
- ✅ No breaking changes

---

## 🎉 All Contributions Welcome!

We appreciate all types of contributions:

| Type | Examples |
|------|----------|
| 🐛 Bug fixes | Fix crashes, errors, edge cases |
| ✨ Features | New functionality, integrations |
| 📚 Documentation | Guides, examples, translations |
| 🎨 UI/UX | Design improvements, accessibility |
| 🧪 Tests | Unit tests, integration tests |
| 💬 Community | Help others, answer questions |

---

<p align="center">
  <strong>Thank you for making Voxelle better! ❤️</strong>
</p>

<p align="center">
  <em>Based on <a href="https://github.com/limitcantcode/jaison-core">J.A.I.son</a> by limitcantcode, merged & enhanced by tulovec96</em>
</p>
